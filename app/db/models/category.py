from tortoise import fields
from tortoise.models import Model


class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class Subcategory(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
