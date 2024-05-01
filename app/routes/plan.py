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


@router.post("/plan", tags=["Plans"], description="New plan", response_model=Plan)
async def post_plan(plan_metadata: PlanMetadata):
    try:
        new_plan = await srv.create_plan(plan_metadata)
        crud.insert_plan(new_plan)
        return new_plan
    except:
        pass


@router.get(
    "/plan/places",
    tags=["Places"],
    description="Get all cities that match with the text",
    response_model=Places,
)
async def get_cities(search_text: str):
    try:
        return srv.get_all_places(search_text)
    except:
        pass
