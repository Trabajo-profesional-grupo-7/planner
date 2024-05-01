import json

from config.database import collection_name

from app.model.plan import Plan


def insert_plan(plan: Plan):
    dict_plan = {}
    for day in plan.plan:
        attractions = plan.plan.get(day)

        daily_attractions = []
        for attraction in attractions:
            daily_attractions.append(
                {
                    "attraction_id": attraction.attraction_id,
                    "attraction_name": attraction.attraction_name,
                    "location": {
                        "latitude": attraction.location["latitude"],
                        "longitude": attraction.location["longitude"],
                    },
                    "date": attraction.date,
                    "hour": None,
                }
            )

        dict_plan[day] = daily_attractions

    collection_name.insert_one(
        {
            "user_id": plan.user_id,
            "plan_name": plan.plan_name,
            "destination": plan.destination,
            "init_date": str(plan.init_date),
            "end_date": str(plan.end_date),
            "plan": dict_plan,
        }
    )
