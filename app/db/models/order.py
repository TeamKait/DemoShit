from tortoise import fields
from tortoise.models import Model

from app.db.models.product import Product
from app.db.models.sizes import Size


class Order(Model):
    id = fields.IntField(pk=True)
    number = fields.IntField()
    date = fields.DateField()
    client = fields.TextField()
    product = fields.ForeignKeyField(
        Product,
        related_name='product',
        on_delete=fields.RESTRICT
    )
    size = fields.ForeignKeyField(
        Size,
        related_name='size',
        on_delete=fields.RESTRICT
    )
