from graphlib import TopologicalSorter

from tortoise import Tortoise


def sorted_models():
    models = [m for app in Tortoise.apps.values() for m in app.values()]
    ts = TopologicalSorter()
    for m in models:
        fields = (*m._meta.fk_fields, *m._meta.o2o_fields)
        deps = {m._meta.fields_map[f].related_model for f in fields}
        ts.add(m, *(d for d in deps if d is not m))
    return list(ts.static_order())
