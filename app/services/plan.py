import os
import urllib.parse
from datetime import timedelta

import requests

from app.model.plan import Attraction, Plan, PlanMetadata
from app.schema.place import Place, Places

USER_SERVICE = os.getenv("USER_SERVICE")
ATTRACTIONS_SERVICE = os.getenv("ATTRACTIONS_SERVICE")


async def create_plan(plan_metadata: PlanMetadata) -> Plan:
    user_preferences = requests.get(
        f"{USER_SERVICE}/users/{plan_metadata.user_id}/preferences",
    )
    user_preferences = user_preferences.json()
    preferences = ",".join(user_preferences)
    preferences = preferences.replace(",", " or ")

    response = requests.post(
        f"{ATTRACTIONS_SERVICE}/attractions/search",
        json={"query": preferences + " in " + plan_metadata.destination},
    )
    attractions = response.json()

    days = (plan_metadata.end_date - plan_metadata.init_date).days

    top_attractions = attractions
    if len(attractions) >= days:
        top_attractions = attractions[:days]

    plan = {}
    date = plan_metadata.init_date
    for attraction in top_attractions:
        latidude = str(attraction["location"]["latitude"])
        longitude = str(attraction["location"]["longitude"])

        url = f"{ATTRACTIONS_SERVICE}/attractions/nearby/{latidude}/{longitude}/{5000}"
        if user_preferences:
            url += "?"
            for type in user_preferences:
                url += f"attraction_types={type}&"

            url = url[: len(url) - 1]

        nearby_attractions = requests.post(url)
        nearby_attractions = nearby_attractions.json()

        top_nearby_attractions = nearby_attractions
        if len(nearby_attractions) >= 2:
            top_nearby_attractions = nearby_attractions[:2]

        daily_attractions_list = []
        for daily_attraction in top_nearby_attractions:
            daily_attractions_list.append(
                Attraction.model_construct(
                    attraction_id=daily_attraction.id,
                    location=daily_attraction.location,
                    date=date,
                    hour=None,
                )
            )

        plan[date] = daily_attractions_list
        date += timedelta(days=1)

    return Plan.model_construct(
        user_id=plan_metadata.user_id,
        plan_name=plan_metadata.plan_name,
        location=plan_metadata.location,
        init_date=plan_metadata.init_date,
        end_date=plan_metadata.end_date,
        plan=plan,
    )


def get_all_places(text: str) -> Places:
    places = requests.post(
        f"{ATTRACTIONS_SERVICE}/attractions/autocomplete", json={"query": text}
    )

    places_list = []
    for place in places.json():
        places_list.append(
            Place.model_construct(
                attraction_id=place["attraction_id"],
                attraction_name=place["attraction_name"],
            )
        )

    return Places.model_construct(places=places_list, total=len(places_list))
