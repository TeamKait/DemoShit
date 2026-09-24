from os import getenv

from tortoise import Tortoise

from app.db.models.order import Order
from app.db.models.product import Product
from app.db.models.user import User


async def connect_db():
    await Tortoise.init(
        db_url=getenv("DSN"),
        modules={'models': [
            'app.db.models.category',
            'app.db.models.manufacturer',
            'app.db.models.order',
            'app.db.models.product',
            'app.db.models.sizes',
            'app.db.models.stock_item',
            'app.db.models.user',
        ]},
        _enable_global_fallback=True,
    )
    await Tortoise.generate_schemas()


class DBService:
    MAX_LIST_ITEMS = 100

    def __init__(self):
        pass

    async def list_products(self, limit: int, offset: int, ascending_order: bool):
        if not limit:
            limit = self.MAX_LIST_ITEMS
        else:
            limit = min(max(limit, 0), self.MAX_LIST_ITEMS)

        order_str = "" if ascending_order else "-"

        products = await (Product
                          .all()
                          .order_by(f'{order_str}id')
                          .limit(limit)
                          .offset(offset))
        # .prefetch_related('name', 'manufacturer', 'category'))
        return products

    async def get_orders(self, limit: int, offset: int, ascending_order: bool):
        if not limit:
            limit = self.MAX_LIST_ITEMS
        else:
            limit = min(max(limit, 0), self.MAX_LIST_ITEMS)

        order_str = "" if ascending_order else "-"

        orders = await Order.all().order_by(f'{order_str}id').limit(limit).offset(offset)
        return orders

    async def get_user_by_login(self, login: str):
        return await User.filter(login=login).first()
