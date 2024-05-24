from bson import ObjectId
from config.database import collection_name
from db import crud
from fastapi import APIRouter
from model.plan import AttractionPlan, Plan, PlanMetadata
from schema.schemas import list_serial
from services import plan as srv

router = APIRouter()


@router.get(
    "/plan/user/{id}", tags=["Plans"], description="Get all plans from an user id"
)
async def get_plans(id: int):
    try:
        return list_serial(collection_name.find({"user_id": id}))
    except:
        pass


@router.get("/plan/{id}", tags=["Plans"], description="Get plan by id")
async def get_plans(id: str):
    try:
        return list_serial(collection_name.find({"_id": ObjectId(id)}))
    except:
        pass


@router.post("/plan", tags=["Plans"], description="New plan", response_model=Plan)
def post_plan(plan_metadata: PlanMetadata):
    try:
        new_plan = srv.create_plan(plan_metadata)
        crud.insert_plan(new_plan)
        return new_plan
    except:
        pass


@router.delete(
    "/plan/attraction", tags=["Plans"], description="Delete attraction from a plan"
)
async def delete_attraction(attraction: AttractionPlan):
    try:
        await srv.delete_attraction(attraction)
    except:
        pass


@router.patch(
    "/plan/attraction", tags=["Plans"], description="Update attraction from a plan"
)
async def update_attraction_plan(attraction: AttractionPlan):
    try:
        await srv.update_attraction_plan(attraction)
    except:
        pass


@router.delete("/plan/{id}", tags=["Plans"], description="Delete plan")
async def delete_plan(id: str):
    try:
        return list_serial(collection_name.delete_one({"_id": ObjectId(id)}))
    except:
        pass
