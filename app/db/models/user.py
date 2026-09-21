from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    role = fields.ForeignKeyField(
        'models.Role',
        related_name='users',
        on_delete=fields.CASCADE
    )
    name = fields.TextField()
    login = fields.TextField()
    password = fields.TextField()


class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
