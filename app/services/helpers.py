import math
from datetime import date
from typing import List

from app.model import plan as model
from app.schema import schemas as dto


def calc_plan_metadata(
    plan_metadata: dto.PlanMetadata,
    attractions: List[model.Attraction],
    user_preferences: List[str],
):
    days = (plan_metadata.end_date - plan_metadata.init_date).days
    if days == 0:
        pass

    attractions_per_day = len(attractions) // days
    attractions_per_day = attractions_per_day if attractions_per_day <= 3 else 3

    total_attactions_amount = attractions_per_day * days
    preferences_amount = len(user_preferences)
    if preferences_amount == 0:
        preferences_amount = 1

    max_type_amount = total_attactions_amount / preferences_amount

    return attractions_per_day, max_type_amount


def calc_distance(attraction_i: model.Attraction, attraction_j: model.Attraction):
    return math.sqrt(
        (attraction_i["location"]["latitude"] - attraction_j["location"]["latitude"])
        ** 2
        + (
            attraction_i["location"]["longitude"]
            - attraction_j["location"]["longitude"]
        )
        ** 2
    )


def check_type_completed(types: dict[str, int], max_type_amount: int, attraction):
    type_completed = False
    for type in attraction["types"]:
        type_amount = types.get(type)
        if not type_amount:
            continue

        if type_amount >= max_type_amount:
            type_completed = True

    return type_completed


def add_attraction(
    assigned_attractions: List[str],
    daily_attractions_list: List[model.Attraction],
    attraction: model.Attraction,
    date: date,
    distances: List[float],
    distance: float,
    types: dict[str, int],
):
    assigned_attractions.append(attraction["attraction_id"])
    daily_attractions_list.append(
        model.Attraction.model_construct(
            attraction_id=attraction["attraction_id"],
            attraction_name=attraction["attraction_name"],
            location=attraction["location"],
            date=str(date),
        )
    )
    distances.append(distance)
    for type in attraction["types"]:
        if types.get(type):
            types[type] += 1
        else:
            types[type] = 1


def remove_attraction(
    distances: List[float],
    max_distance: float,
    daily_attractions_list: List,
    assigned_attractions: List[str],
    attractions: List,
    types: dict[str, int],
):
    to_remove = distances.index(max_distance)
    distance = distances.pop(to_remove)
    removed_attraction = daily_attractions_list.pop(to_remove)
    assigned_attractions.remove(removed_attraction.attraction_id)

    for attraction in attractions:
        if attraction["attraction_id"] == removed_attraction.attraction_id:
            break

    for type in attraction["types"]:
        type_amount = types.get(type)
        if type_amount == 1:
            types.pop(type)
        else:
            types[type] -= 1
