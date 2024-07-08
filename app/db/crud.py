from typing import List

from bson import ObjectId
from config.database import plans_collection

from app.exceptions.exceptions import InvalidAttractionID, PlanNotFound
from app.model.plan import Plan


def insert_plan(plan: Plan) -> str:
    result = plans_collection.insert_one(plan)
    return result.inserted_id


def get_plan_by_id(id: str) -> Plan:
    try:
        plan = plans_collection.find_one({"_id": ObjectId(id)})
        if not plan:
            raise PlanNotFound()

        return plan
    except:
        raise InvalidAttractionID()


def get_plans_by_user_id(user_id: str) -> List[Plan]:
    return plans_collection.find({"user_id": user_id})


def get_plan_by_name(user_id: str, plan_name: str) -> Plan:
    try:
        plan = plans_collection.find_one({"user_id": user_id, "plan_name": plan_name})
        if not plan:
            raise PlanNotFound()

        return plan
    except:
        raise InvalidAttractionID()


def delete_plan_by_id(id: str) -> int:
    try:
        result = plans_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count
    except:
        raise InvalidAttractionID()


def update_plan(id: str, plan: Plan):
    try:
        plans_collection.update_one({"_id": ObjectId(id)}, {"$set": plan})
    except:
        raise InvalidAttractionID()
