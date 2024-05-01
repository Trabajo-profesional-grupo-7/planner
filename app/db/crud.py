from config.database import collection_name

from app.model.plan import Plan


def insert_plan(plan: Plan):
    collection_name.insert_one(plan)
