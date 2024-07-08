import math
import os
from datetime import timedelta

from db import crud
from fastapi import HTTPException

from app.model.plan import Plan
from app.schema import parser
from app.schema import schemas as dto
from app.services import api, helpers

ATTRACTIONS_URL = os.getenv("ATTRACTIONS_URL")


# Arma un plan agrupando las atracciones por día que esté más cercanas entre sí.
# Reparte de forma equitativa los tipos de atracciones según las preferencias del usuario.
def create_plan(plan_metadata: dto.PlanMetadata) -> dict:
    user_preferences = api.get_user_preferences(plan_metadata.user_id)
    attractions = api.get_recommended_attractions(
        plan_metadata.user_id, plan_metadata.destination, user_preferences
    )

    attractions_per_day, max_type_amount = helpers.calc_plan_metadata(
        plan_metadata,
        attractions,
        user_preferences,
    )

    user_plan = {}
    date = plan_metadata.init_date
    assigned_attractions = []
    types = {}

    for i in range(0, len(attractions) - 1):
        if date == plan_metadata.end_date:
            break

        daily_attractions_list = []
        distances = []

        for j in range(0, len(attractions)):
            if (
                helpers.check_type_completed(types, max_type_amount, attractions[j])
                or attractions[j]["attraction_id"] in assigned_attractions
            ):
                continue

            distance = helpers.calc_distance(attractions[i], attractions[j])

            if distances:
                max_distance = max(distances)
            else:
                max_distance = 1

            if (
                distance < max_distance
                or len(daily_attractions_list) < attractions_per_day
            ):
                helpers.add_attraction(
                    assigned_attractions,
                    daily_attractions_list,
                    attractions[j],
                    date,
                    distances,
                    distance,
                    types,
                )

                if len(daily_attractions_list) > attractions_per_day:
                    helpers.remove_attraction(
                        distances,
                        max_distance,
                        daily_attractions_list,
                        assigned_attractions,
                        attractions,
                        types,
                    )

        user_plan[str(date)] = daily_attractions_list
        date += timedelta(days=1)

    new_plan = Plan(
        user_id=plan_metadata.user_id,
        plan_name=plan_metadata.plan_name,
        destination=plan_metadata.destination,
        init_date=plan_metadata.init_date,
        end_date=plan_metadata.end_date,
        attractions=assigned_attractions,
        plan=user_plan,
    )
    new_plan = parser.parse_plan(new_plan)
    plan_id = crud.insert_plan(new_plan)
    new_plan["id"] = str(plan_id)

    return str(plan_id)


def delete_attraction(attr_to_remove: dto.AttractionPlan):
    plan = crud.get_plan_by_id(attr_to_remove.plan_id)

    daily_attractions = plan["plan"][attr_to_remove.date]

    for attraction in daily_attractions:
        if attraction["attraction_id"] == attr_to_remove.attraction_id:
            daily_attractions.remove(attraction)

    crud.update_plan(attr_to_remove.plan_id, plan)


def update_attraction_plan(attr_to_update: dto.AttractionPlan):
    plan = crud.get_plan_by_id(attr_to_update.plan_id)

    user_preferences = api.get_user_preferences(plan["user_id"])
    day = plan["plan"][attr_to_update.date]

    for attraction in day:
        if attraction["attraction_id"] == attr_to_update.attraction_id:
            nearby_attractions = api.get_nearby_attractions(
                user_preferences=user_preferences,
                latitude=attraction["location"]["latitude"],
                longitude=attraction["location"]["longitude"],
                radius=5000,
            )

            for attraction in nearby_attractions:
                if not attraction["attraction_id"] in plan["attractions"]:
                    plan["attractions"].append(attraction["attraction_id"])
                    day.append(
                        {
                            "attraction_id": attraction["attraction_id"],
                            "attraction_name": attraction["attraction_name"],
                            "location": attraction["location"],
                            "date": attr_to_update.date,
                            "hour": None,
                        }
                    )
                    crud.update_plan(attr_to_update.plan_id, plan)
                    delete_attraction(attr_to_update)
                    break
