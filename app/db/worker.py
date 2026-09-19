import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from app.auth.service import AuthService
from app.db.service import connect_db


class DBWorker(QObject):
    auth_result = pyqtSignal(bool)
    auth_error = pyqtSignal(str)
    finished = pyqtSignal()

    LOGIN_TIMEOUT = 5.0

    def __init__(self, db_service):
        super().__init__()
        self.db_service = db_service
        self.auth_service = AuthService(db_service)
        self.loop = None
        self._thread = None
        self.executor = ThreadPoolExecutor(max_workers=2)

    def start_worker(self):
        if self._thread is not None:
            return
        self.loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(connect_db())
        except Exception as e:
            self.auth_error.emit(f"Database connection error: {e}")
        self.loop.run_forever()

    @pyqtSlot(str, str)
    def authenticate(self, login, password):
        if not self.loop or not self.loop.is_running():
            self.auth_error.emit("Worker not initialized")
            return

        async def _run_auth_with_timeout():
            try:
                print("[Worker] Запуск задачи авторизации...")

                login_callable = self.auth_service.login
                auth_coro = login_callable(login, password)

                if asyncio.iscoroutine(auth_coro):
                    return await asyncio.wait_for(auth_coro, timeout=self.LOGIN_TIMEOUT)
                else:
                    return await asyncio.wait_for(
                        self.loop.run_in_executor(self.executor, login_callable, login, password),
                        timeout=self.LOGIN_TIMEOUT,
                    )

            except (asyncio.TimeoutError, TimeoutError):
                print(f"[Worker] Ошибка: превышен таймаут в {self.LOGIN_TIMEOUT} сек!")
                raise TimeoutError("Login request timed out")
            except Exception as e:
                import traceback
                print("[Worker] Критическая ошибка внутри задачи:")
                traceback.print_exc()
                raise e

        future = asyncio.run_coroutine_threadsafe(_run_auth_with_timeout(), self.loop)

        def callback(fut):
            try:
                result = fut.result()
                print(f"[Worker] Результат получен: {result}")
                self.auth_result.emit(result)
            except TimeoutError:
                self.auth_error.emit("Timeout")
            except Exception:
                self.auth_error.emit("Error during login execution")

        future.add_done_callback(callback)

    @pyqtSlot()
    def stop_worker(self):
        if self.loop and self.loop.is_running():
            async def _close():
                from tortoise import Tortoise
                try:
                    await Tortoise.close_connections()
                except Exception:
                    pass
                finally:
                    self.loop.call_soon_threadsafe(self.loop.stop)

            asyncio.run_coroutine_threadsafe(_close(), self.loop)
            self._thread.join(timeout=3)

        self.executor.shutdown(wait=False)
        self.finished.emit()
