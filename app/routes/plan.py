from typing import List

from db import crud
from fastapi import APIRouter, HTTPException, Response, status
from schema import parser
from services import plan as srv

from app.schema import schemas as dto

router = APIRouter()


@router.get(
    "/plan/user/{id}",
    tags=["Get plans"],
    description="Get all plans from an user id",
    response_model=List[dto.Plan] | str,
    status_code=status.HTTP_200_OK,
)
async def get_plans(id: int):
    try:
        db_plans = crud.get_plans_by_user_id(id)
        return parser.parse_plan_list(db_plans)
    except Exception as e:
        print(e)


@router.get(
    "/plan/{id}",
    tags=["Get plans"],
    description="Get plan by id",
    response_model=dto.Plan | str,
    status_code=status.HTTP_200_OK,
)
async def get_plans(id: str, response: Response):
    try:
        plan = crud.get_plan_by_id(id)
        if not plan:
            raise HTTPException(status_code=400, detail="Plan not found")
        return parser.parse_plan_dto(plan)
    except HTTPException as e:
        response.status_code = e.status_code
        return e.detail


@router.post(
    "/plan",
    tags=["Create plan"],
    description="Create a new plan",
    response_model=dto.Plan | str,
    status_code=status.HTTP_201_CREATED,
)
def post_plan(plan_metadata: dto.PlanMetadata, response: Response):
    try:
        return srv.create_plan(plan_metadata)
    except HTTPException as e:
        response.status_code = e.status_code
        return e.detail


@router.delete(
    "/plan/attraction",
    tags=["Update plan"],
    description="Delete attraction from a plan",
    status_code=status.HTTP_200_OK,
)
async def delete_attraction(attraction: dto.AttractionPlan):
    try:
        srv.delete_attraction(attraction)
    except:
        pass


@router.patch(
    "/plan/attraction",
    tags=["Update plan"],
    description="Update attraction from a plan",
    status_code=status.HTTP_200_OK,
)
async def update_attraction_plan(attraction: dto.AttractionPlan):
    try:
        srv.update_attraction_plan(attraction)
    except Exception as e:
        print(e)


@router.delete(
    "/plan/{id}",
    tags=["Delete plan"],
    description="Delete plan",
    status_code=status.HTTP_200_OK,
)
async def delete_plan(id: str, response: Response):
    try:
        if crud.delete_plan_by_id(id):
            return "Plan deleted"

        raise HTTPException(status_code=400, detail="Plan not found")
    except HTTPException as e:
        response.status_code = e.status_code
        return e.detail
