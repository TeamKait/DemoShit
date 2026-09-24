from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    surname = fields.TextField()
    name = fields.TextField()
    patronym = fields.TextField()
    login = fields.TextField()
    role = fields.ForeignKeyField(
        'models.Role',
        related_name='users',
        on_delete=fields.CASCADE
    )


class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
