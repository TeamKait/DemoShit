from tortoise import fields
from tortoise.models import Model

from app.db.models.product import Product


class Order(Model):
    id = fields.IntField(pk=True)
    article1: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField(
        "models.Product",
        related_name="orders_as_first",
        to_field="article",
        on_delete=fields.RESTRICT
    )
    article1_amount = fields.IntField()
    article2: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField(
        "models.Product",
        related_name="orders_as_second",
        to_field="article",
        on_delete=fields.RESTRICT
    )
    article2_amount = fields.IntField()
    order_date = fields.DateField()
    delivery_date = fields.DateField()
    address = fields.TextField()
    client = fields.TextField()
    code = fields.IntField()
    status = fields.OneToOneField(
        "models.Status",
        related_name="order",
        on_delete=fields.CASCADE
    )


class Status(Model):
    id = fields.IntField(pk=True)
    status = fields.TextField()
