from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from qasync import asyncSlot

from app.db.service import DBService


class ProductsViewPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.db = DBService()

        self.label = QLabel(self)
        self.label.setText("Test")

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.setLayout(layout)

        self.init()

    @asyncSlot()
    async def init(self):
        products = await self.db.list_products(100, 0, True)
        text = ""
        for product in products:
            text += f"{product.id} - {product.name.name}\n"
        self.label.setText(text)
