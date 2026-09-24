import asyncio
import sys
import traceback

from PyQt6.QtWidgets import (
    QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel,
)
from qasync import asyncSlot

from app.db.service import DBService


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "".join(traceback.format_exception(ex_cls, ex, tb))
    print("Error:\n", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class AuthPage(QWidget):
    LOGIN_TIMEOUT = 5.0

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db = DBService()

        self.label = QLabel("Auth test", self)
        self.login_input = QLineEdit(self)
        self.button = QPushButton("Click Me", self)

        self.button.clicked.connect(self.on_button_click)
        self.login_input.returnPressed.connect(self.on_button_click)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    @asyncSlot()
    async def on_button_click(self):
        login = self.login_input.text().strip()

        self.button.setEnabled(False)
        self.label.setText("Checking...")

        try:
            user = await asyncio.wait_for(
                self.db.get_user_by_login(login),
                timeout=self.LOGIN_TIMEOUT,
            )
        except TimeoutError:
            self.label.setText("Превышено время ожидания")
        except Exception as e:
            print(f"Login error: {e}")
            self.label.setText("Ошибка авторизации")
        else:
            if user is not None and user.exists():
                self.stacked_widget.setCurrentIndex(1)
            else:
                self.label.setText("Failed")

        finally:
            self.button.setEnabled(True)
