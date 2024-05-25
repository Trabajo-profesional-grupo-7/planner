from config.database import collection_name

from app.model.plan import Plan
from app.schema.schemas import deserialize


def insert_plan(plan: Plan):
    dict_plan = deserialize(plan)
    collection_name.insert_one(dict_plan)


def get_plan_by_name(user_id: int, plan_name: str):
    return collection_name.find_one({"user_id": user_id, "plan_name": plan_name})
