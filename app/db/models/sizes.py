from tortoise import fields
from tortoise.models import Model


class Size(Model):
    id = fields.IntField(pk=True)
    value = fields.FloatField()
