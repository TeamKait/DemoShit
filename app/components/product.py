from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel
)

from app.db.models.product import Product


class ProductItemWidget(QWidget):
    def __init__(self, prod: Product):
        super().__init__()

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(15)

        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 75)
        self.image_label.setStyleSheet("border: 2px solid black; border-radius: 4px;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if prod.photo:
            pixmap = QPixmap(prod.photo)

            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("🖼️")
            font = self.image_label.font()
            font.setPointSize(24)
            self.image_label.setFont(font)

        main_layout.addWidget(self.image_label)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(4)

        top_row_layout = QHBoxLayout()

        self.title_label = QLabel(prod.manufacturer.name)
        title_font = QFont()
        title_font.setPointSize(14)
        self.title_label.setFont(title_font)

        self.price_label = QLabel(str(prod.price))
        price_font = QFont()
        price_font.setPointSize(16)
        self.price_label.setFont(price_font)
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        top_row_layout.addStretch()
        top_row_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        top_row_layout.addStretch()
        top_row_layout.addWidget(self.price_label)

        content_layout.addLayout(top_row_layout)

        details_layout = QVBoxLayout()
        details_layout.setSpacing(2)

        self.cat_label = QLabel(f"Категория: {prod.category.name}")
        # self.count_label = QLabel(f"Количество: {prod.}")
        self.style_label = QLabel(f"Состав: {prod.composition}")

        detail_style = "color: #333333; font-size: 12px;"
        for label in (self.cat_label, self.style_label):
            label.setStyleSheet(detail_style)
            details_layout.addWidget(label)

        content_layout.addLayout(details_layout)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
