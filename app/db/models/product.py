from tortoise import fields
from tortoise.models import Model

from app.db.models.category import Category, Subcategory
from app.db.models.manufacturer import Manufacturer


class Product(Model):
    id = fields.IntField(pk=True)
    category = fields.ForeignKeyField(
        Category,
        related_name='category',
        on_delete=fields.CASCADE
    )
    subcategory = fields.ForeignKeyField(
        Subcategory,
        related_name='subcategory',
        on_delete=fields.CASCADE
    )
    photo = fields.TextField(null=True)
    name = fields.TextField()
    manufacturer = fields.ForeignKeyField(
        Manufacturer,
        related_name='manufacturer',
        on_delete=fields.CASCADE
    )
    description = fields.TextField()
    composition = fields.TextField()
    price = fields.IntField()
