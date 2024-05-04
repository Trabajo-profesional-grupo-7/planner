from app.model.plan import Plan


def parse_plan(plan: Plan) -> dict:
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

    return {
        "user_id": plan.user_id,
        "plan_name": plan.plan_name,
        "destination": plan.destination,
        "init_date": str(plan.init_date),
        "end_date": str(plan.end_date),
        "attractions": plan.attractions,
        "plan": dict_plan,
    }
