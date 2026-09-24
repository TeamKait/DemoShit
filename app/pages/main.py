from PyQt6.QtWidgets import QStackedWidget

from app.pages.auth import AuthPage
from app.pages.products import ProductsViewPage


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.auth_window = AuthPage(self)
        self.addWidget(self.auth_window)

        self.products_page = ProductsViewPage(self)
        self.addWidget(self.products_page)

        self.setCurrentIndex(0)

        self.setWindowTitle("DemoShit")
        self.resize(300, 150)
