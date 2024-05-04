from bson import ObjectId
from config.database import collection_name
from db import crud
from fastapi import APIRouter
from helpers import plan as helper
from model.plan import Plan, PlanMetadata
from schema.schemas import list_serial
from services import plan as srv

from app.schema.place import Places

router = APIRouter()


@router.get(
    "/plan/user/{id}", tags=["Plans"], description="Get all plans from an user id"
)
async def get_plans(user_id: int):
    try:
        return list_serial(collection_name.find({"user_id": user_id}))
    except:
        pass


@router.get("/plan/{id}", tags=["Plans"], description="Get plan by id")
async def get_plans(plan_id: str):
    try:
        return list_serial(collection_name.find({"_id": ObjectId(plan_id)}))
    except:
        pass


@router.post("/plan", tags=["Plans"], description="New plan", response_model=Plan)
async def post_plan(plan_metadata: PlanMetadata):
    try:
        new_plan = await srv.create_plan(plan_metadata)
        crud.insert_plan(new_plan)
        return new_plan
    except:
        pass
