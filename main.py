import asyncio
import sys

from PyQt6.QtWidgets import QApplication
from dotenv import load_dotenv
from qasync import QEventLoop
from tortoise import Tortoise

from app.db.service import connect_db
from app.pages.main import MainWindow


async def main(app: QApplication) -> None:
    await connect_db()

    app.setQuitOnLastWindowClosed(False)

    window = MainWindow()
    window.show()

    last_window_closed = asyncio.Event()
    app.lastWindowClosed.connect(last_window_closed.set)

    await last_window_closed.wait()

    await Tortoise.close_connections()

    app.quit()


if __name__ == "__main__":
    load_dotenv()

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    with loop:
        loop.run_until_complete(main(app))
