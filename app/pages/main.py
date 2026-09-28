from PyQt6.QtWidgets import QStackedWidget, QWidget, QSizePolicy

from app.pages.auth import AuthPage


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DemoShit")

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.current_page = AuthPage(self)
        self.addWidget(self.current_page)
        self.setCurrentIndex(0)

        self.resize(300, 150)

    def switch_page(self, next_page: QWidget):
        if not next_page:
            return

        old_page = self.currentWidget()

        new_index = self.addWidget(next_page)

        self.setCurrentIndex(new_index)

        self.current_page = next_page

        if old_page:
            self.removeWidget(old_page)
            old_page.deleteLater()

        self.updateGeometry()
        self.adjustSize()
