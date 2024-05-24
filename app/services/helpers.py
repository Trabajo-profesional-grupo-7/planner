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
    attractions_amount,
    restricted_attractions,
):
    nearby_attractions = requests.post(
        url=f"{ATTRACTIONS_URL}/attractions/nearby/{latitude}/{longitude}/{radius}",
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
