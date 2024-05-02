from config.database import collection_name

from app.helpers.plan import parse_plan
from app.model.plan import Plan


def insert_plan(plan: Plan):
    dict_plan = parse_plan(plan)
    collection_name.insert_one(dict_plan)
