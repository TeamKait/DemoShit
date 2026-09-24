from tortoise import Model, fields

from app.db.models.sizes import Size


class StockItem(Model):
    id = fields.IntField(pk=True)
    size = fields.ForeignKeyField(
        Size,
        related_name='stock_item',
        on_delete=fields.CASCADE
    )
    available = fields.IntField()
