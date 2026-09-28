import asyncio
import json

from tortoise import Tortoise

from app.db.service import TORTOISE_CONFIG
from scripts.common import sorted_models


async def main():
    await Tortoise.init(config=TORTOISE_CONFIG)
    data = {m._meta.db_table: await m.all().values()
            for m in sorted_models()}
    with open("dump.json", "w", encoding="utf-8") as f:
        json.dump(data, f, default=str, ensure_ascii=False)
    await Tortoise.close_connections()


asyncio.run(main())
