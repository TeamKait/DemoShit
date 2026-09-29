from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from qasync import asyncSlot

from app.components.product import ProductItemWidget
from app.db.service import DBService


class ProductsPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.db = DBService()

        self.label = QLabel(self)
        self.label.setText("Test")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(self.layout)

        self.setLayout(self.layout)

        self.init()

    @asyncSlot()
    async def init(self):
        products = await self.db.list_products(100, 0, True)
        for p in products:
            self.layout.addWidget(ProductItemWidget(p))
