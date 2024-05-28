import os

import requests

USER_SERVICE = os.getenv("USER_SERVICE")
ATTRACTIONS_URL = os.getenv("ATTRACTIONS_URL")


def get_user_preferences(user_id: int):
    user_preferences = requests.get(
        f"{USER_SERVICE}/users/{user_id}/preferences",
    )
    return user_preferences.json()


def get_google_top_attractions(user_preferences, destination) -> list:
    preferences = ",".join(user_preferences)
    preferences = preferences.replace(",", " or ")

    attractions = requests.post(
        f"{ATTRACTIONS_URL}/attractions/search",
        json={"query": preferences + " in " + destination},
    )

    return list(attractions.json())


def get_recommended_attractions(user_id, destination, user_preferences=[]) -> list:
    attractions = requests.post(
        f"{ATTRACTIONS_URL}/create_plan/",
        json={
            "user_id": user_id,
            "city": destination,
            "preferences": user_preferences,
        },
    )

    return list(attractions.json())


def get_nearby_attractions(
    user_preferences,
    latitude,
    longitude,
    radius,
):
    nearby_attractions = requests.post(
        url=f"{ATTRACTIONS_URL}/attractions/nearby/{latitude}/{longitude}/{radius}",
        json={"attraction_types": user_preferences},
    )
    return list(nearby_attractions.json())
