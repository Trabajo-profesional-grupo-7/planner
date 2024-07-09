from typing import List

from fastapi import APIRouter, Response, status

from app.config import logging
from app.db import crud
from app.exceptions.api_exception import APIException
from app.schema import parser
from app.schema import schemas as dto
from app.services import plan as srv

logger = logging.get_logger()

router = APIRouter()


@router.get(
    "/plan/user/{id}",
    tags=["Get plans"],
    description="Get all plans from an user id",
    response_model=List[dto.Plan] | str,
    status_code=status.HTTP_200_OK,
)
async def get_plans(id: int, response: Response):
    try:
        db_plans = crud.get_plans_by_user_id(id)
        return parser.parse_plan_list(db_plans)
    except APIException as e:
        response.status_code = e.error_code
        return e.detail


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
        return parser.parse_plan_dto(plan)
    except APIException as e:
        response.status_code = e.error_code
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
        plan = srv.create_plan(plan_metadata)
        logger.info(f"New plan created for user {plan_metadata.user_id}.")
        return plan
    except APIException as e:
        logger.error(f"Error creating plan for user {plan_metadata.user_id}.")
        response.status_code = e.error_code
        return e.detail


@router.delete(
    "/plan/attraction",
    tags=["Update plan"],
    description="Delete attraction from a plan",
    status_code=status.HTTP_200_OK,
)
async def delete_attraction(attraction: dto.AttractionPlan, response: Response):
    try:
        srv.delete_attraction(attraction)
        logger.info(
            f"Attraction {attraction.attraction_id} deleted from plan {attraction.plan_id}."
        )
    except APIException as e:
        logger.error(
            f"Error deleting attraction {attraction.attraction_id} from plan {attraction.plan_id}."
        )
        response.status_code = e.error_code
        return e.detail


@router.patch(
    "/plan/attraction",
    tags=["Update plan"],
    description="Update attraction from a plan",
    status_code=status.HTTP_200_OK,
)
async def update_attraction_plan(attraction: dto.AttractionPlan, response: Response):
    try:
        srv.update_attraction_plan(attraction)
        logger.info(
            f"Attraction {attraction.attraction_id} updated in plan {attraction.plan_id}."
        )
    except APIException as e:
        logger.error(
            f"Error updating attraction {attraction.attraction_id} from plan {attraction.plan_id}."
        )
        response.status_code = e.error_code
        return e.detail


@router.delete(
    "/plan/{id}",
    tags=["Delete plan"],
    description="Delete plan",
    status_code=status.HTTP_200_OK,
)
async def delete_plan(id: str, response: Response):
    try:
        crud.delete_plan_by_id(id)
        logger.info(f"Plan {id} deleted.")
    except APIException as e:
        logger.error(f"Error deleting plan {id}.")
        response.status_code = e.error_code
        return e.detail
