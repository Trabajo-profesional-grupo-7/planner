import math
import os
from datetime import timedelta

import requests
from bson import ObjectId
from config.database import collection_name
from services import helpers

from app.model.plan import Attraction, AttractionPlan, Plan, PlanMetadata

ATTRACTIONS_URL = os.getenv("ATTRACTIONS_URL")


def get_google_top_attractions(user_preferences, destination, days):
    preferences = ",".join(user_preferences)
    preferences = preferences.replace(",", " or ")

    attractions = requests.post(
        f"{ATTRACTIONS_URL}/attractions/search",
        json={"query": preferences + " in " + destination},
    )

    top_attractions = attractions.json()
    if len(attractions) >= days:
        top_attractions = attractions[:days]

    return top_attractions


def create_plan(plan_metadata: PlanMetadata) -> Plan:
    user_preferences = helpers.get_user_preferences(plan_metadata.user_id)

    days = (plan_metadata.end_date - plan_metadata.init_date).days
    attractions = helpers.get_recommended_attractions(
        plan_metadata.user_id, plan_metadata.destination, user_preferences
    )

    attractions_per_day = len(attractions) // days
    attractions_per_day = attractions_per_day if attractions_per_day <= 3 else 3

    user_plan = {}
    date = plan_metadata.init_date
    assigned_attractions = []
    for i in range(0, len(attractions) - 1):

        if date == plan_metadata.end_date:
            break

        daily_attractions_list = []
        distances = []

        for j in range(0, len(attractions)):
            if attractions[j]["attraction_id"] in assigned_attractions:
                continue

            distance = math.sqrt(
                (
                    attractions[i]["location"]["latitude"]
                    - attractions[j]["location"]["latitude"]
                )
                ** 2
                + (
                    attractions[i]["location"]["longitude"]
                    - attractions[j]["location"]["longitude"]
                )
                ** 2
            )

            if distances:
                max_distance = max(distances)
            else:
                max_distance = 1

            if (
                distance < max_distance
                or len(daily_attractions_list) < attractions_per_day
            ):
                assigned_attractions.append(attractions[j]["attraction_id"])
                daily_attractions_list.append(
                    Attraction.model_construct(
                        attraction_id=attractions[j]["attraction_id"],
                        attraction_name=attractions[j]["attraction_name"],
                        location=attractions[j]["location"],
                        date=str(date),
                    )
                )
                distances.append(distance)

                if len(daily_attractions_list) > attractions_per_day:
                    to_remove = distances.index(max_distance)
                    distance = distances.pop(to_remove)
                    attraction = daily_attractions_list.pop(to_remove)
                    assigned_attractions.remove(attraction.attraction_id)

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

    user_preferences = helpers.get_user_preferences(plan["user_id"])
    day = plan["plan"][attr_to_update.date]

    for attraction in day:
        if attraction["attraction_id"] == attr_to_update.attraction_id:
            new_attraction = helpers.get_nearby_attractions(
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
