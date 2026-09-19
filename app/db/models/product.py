from tortoise import fields
from tortoise.models import Model


class Product(Model):
    id = fields.IntField(pk=True)
    article = fields.CharField(max_length=16, unique=True, index=True)
    name = fields.OneToOneField(
        'models.ProductName',
        related_name='product',
        on_delete=fields.CASCADE
    )
    measurement = fields.TextField()
    price = fields.IntField()
    supplier = fields.OneToOneField(
        'models.Supplier',
        related_name='supplier',
        on_delete=fields.CASCADE
    )
    manufacturer = fields.OneToOneField(
        'models.Manufacturer',
        related_name='manufacturer',
        on_delete=fields.CASCADE
    )
    category = fields.OneToOneField(
        'models.Category',
        related_name='category',
        on_delete=fields.CASCADE
    )
    discount = fields.IntField()
    amount = fields.IntField()
    description = fields.TextField()
    photo = fields.TextField(null=True)


class ProductName(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class Supplier(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class Manufacturer(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
