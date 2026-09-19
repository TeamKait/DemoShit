import asyncio
import sys
import traceback

from PyQt6.QtWidgets import (
    QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel,
)
from qasync import asyncSlot

from app.auth.service import AuthService
from app.db.service import DBService


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "".join(traceback.format_exception(ex_cls, ex, tb))
    print("Error:\n", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class MainWindow(QMainWindow):
    LOGIN_TIMEOUT = 5.0

    def __init__(self):
        super().__init__()
        self.auth_service = AuthService(DBService())

        self.setWindowTitle("DemoShit")
        self.resize(300, 150)

        self.label = QLabel("Auth test", self)
        self.login_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.button = QPushButton("Click Me", self)

        self.button.clicked.connect(self.on_button_click)
        self.login_input.returnPressed.connect(self.on_button_click)
        self.password_input.returnPressed.connect(self.on_button_click)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @asyncSlot()
    async def on_button_click(self):
        login = self.login_input.text().strip()
        passwd = self.password_input.text().strip()

        self.button.setEnabled(False)
        self.label.setText("Checking...")

        try:
            ok = await asyncio.wait_for(
                self.auth_service.login(login, passwd),
                timeout=self.LOGIN_TIMEOUT,
            )
        except TimeoutError:
            self.label.setText("Превышено время ожидания")
        except Exception as e:
            print(f"Login error: {e}")
            self.label.setText("Ошибка авторизации")
        else:
            self.label.setText("Success" if ok else "Failed")
        finally:
            self.button.setEnabled(True)
