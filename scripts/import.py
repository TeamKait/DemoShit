import asyncio
import json

from tortoise import Tortoise
from tortoise.fields import IntField, BigIntField, SmallIntField

from app.db.service import TORTOISE_CONFIG
from scripts.common import sorted_models


async def main():
    await Tortoise.init(config=TORTOISE_CONFIG)
    await Tortoise.generate_schemas()
    conn = Tortoise.get_connection("default")
    with open("dump.json", encoding="utf-8") as f:
        data = json.load(f)

    for m in sorted_models():
        table = m._meta.db_table
        rows = data.get(table, [])
        if not rows:
            continue
        await m.bulk_create([m(**r) for r in rows], batch_size=500)

        if isinstance(m._meta.pk, (IntField, BigIntField, SmallIntField)):
            pk = m._meta.db_pk_column
            await conn.execute_query(
                f"SELECT setval(pg_get_serial_sequence('\"{table}\"', '{pk}'), "
                f"(SELECT MAX(\"{pk}\") FROM \"{table}\"))"
            )
    await Tortoise.close_connections()


asyncio.run(main())
