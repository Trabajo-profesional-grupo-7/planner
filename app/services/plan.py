import os
from datetime import timedelta

import requests
from bson import ObjectId
from config.database import collection_name

from app.model.plan import Attraction, AttractionPlan, Plan, PlanMetadata
from app.schema import schemas

USER_SERVICE = os.getenv("USER_SERVICE")
ATTRACTIONS_SERVICE = os.getenv("ATTRACTIONS_SERVICE")


async def create_plan(plan_metadata: PlanMetadata) -> Plan:
    user_preferences = get_user_preferences(plan_metadata.user_id)

    days = (plan_metadata.end_date - plan_metadata.init_date).days

    top_attractions = get_user_top_attractions(
        user_preferences, plan_metadata.destination, days
    )

    user_plan = {}
    date = plan_metadata.init_date
    assigned_attractions = []
    for attraction in top_attractions:
        daily_attractions_list = []
        assigned_attractions.append(attraction["attraction_id"])
        daily_attractions_list.append(
            Attraction.model_construct(
                attraction_id=attraction["attraction_id"],
                attraction_name=attraction["attraction_name"],
                location=attraction["location"],
                date=str(date),
            )
        )

        top_nearby_attractions = get_nearby_attractions(
            user_preferences=user_preferences,
            latitude=str(attraction["location"]["latitude"]),
            longitude=str(attraction["location"]["longitude"]),
            radius=5000,
            attractions_amount=2,
            restricted_attractions=assigned_attractions,
        )

        for daily_attraction in top_nearby_attractions:
            assigned_attractions.append(daily_attraction["attraction_id"])
            daily_attractions_list.append(
                Attraction.model_construct(
                    attraction_id=daily_attraction["attraction_id"],
                    attraction_name=daily_attraction["attraction_name"],
                    location=daily_attraction["location"],
                    date=str(date),
                )
            )

        user_plan[str(date)] = daily_attractions_list
        date += timedelta(days=1)

    return Plan(
        user_id=plan_metadata.user_id,
        plan_name=plan_metadata.plan_name,
        destination=plan_metadata.destination,
        init_date=plan_metadata.init_date,
        end_date=plan_metadata.end_date,
        attractions=assigned_attractions,
        plan=user_plan,
    )


def delete_attraction(attr_to_remove: AttractionPlan):
    plan = collection_name.find_one({"_id": ObjectId(attr_to_remove.plan_id)})

    day = plan["plan"][attr_to_remove.date]

    for attraction in day:
        if attraction["attraction_id"] == attr_to_remove.attraction_id:
            day.remove(attraction)

    collection_name.update_one(
        {"_id": ObjectId(attr_to_remove.plan_id)}, {"$set": plan}
    )


def update_attraction_plan(attr_to_update: AttractionPlan):
    plan = collection_name.find_one({"_id": ObjectId(attr_to_update.plan_id)})

    user_preferences = get_user_preferences(plan["user_id"])
    day = plan["plan"][attr_to_update.date]

    for attraction in day:
        if attraction["attraction_id"] == attr_to_update.attraction_id:
            new_attraction = get_nearby_attractions(
                user_preferences=user_preferences,
                latitude=attraction["location"]["latitude"],
                longitude=attraction["location"]["longitude"],
                radius=5000,
                attractions_amount=1,
                restricted_attractions=plan["attractions"],
            )[0]

            plan["attractions"].append(new_attraction["attraction_id"])
            day.append(new_attraction)
            break

    collection_name.update_one(
        {"_id": ObjectId(attr_to_update.plan_id)}, {"$set": plan}
    )
    delete_attraction(attr_to_update)


def get_user_preferences(user_id: int):
    user_preferences = requests.get(
        f"{USER_SERVICE}/users/{user_id}/preferences",
    )
    return user_preferences.json()


def get_user_top_attractions(user_preferences, destination, days):
    preferences = ",".join(user_preferences)
    preferences = preferences.replace(",", " or ")

    attractions = requests.post(
        f"{ATTRACTIONS_SERVICE}/attractions/search",
        json={"query": preferences + " in " + destination},
    )
    attractions = attractions.json()

    top_attractions = attractions
    if len(attractions) >= days:
        top_attractions = attractions[:days]

    return top_attractions


def get_nearby_attractions(
    user_preferences,
    latitude,
    longitude,
    radius,
    attractions_amount,
    restricted_attractions,
):
    nearby_attractions = requests.post(
        url=f"{ATTRACTIONS_SERVICE}/attractions/nearby/{latitude}/{longitude}/{radius}",
        json={"attraction_types": user_preferences},
    )
    nearby_attractions = list(nearby_attractions.json())

    top_nearby_attractions = 0
    new_attractions = []
    for attraction in nearby_attractions:
        if top_nearby_attractions == attractions_amount:
            break

        if not attraction["attraction_id"] in restricted_attractions:
            new_attractions.append(attraction)
            top_nearby_attractions += 1

    return new_attractions
