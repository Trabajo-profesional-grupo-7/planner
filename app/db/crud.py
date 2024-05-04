from config.database import collection_name

from app.model.plan import Plan
from app.schema.schemas import deserialize


def insert_plan(plan: Plan):
    dict_plan = deserialize(plan)
    collection_name.insert_one(dict_plan)
