from app.model import plan as model
from app.schema import schemas as schema


def parse_plan(plan: model.Plan):
    dict_plan = {}
    for day in plan["plan"]:
        attractions = plan["plan"].get(day)

        daily_attractions = []
        for attraction in attractions:
            daily_attractions.append(
                {
                    "attraction_id": attraction["attraction_id"],
                    "attraction_name": attraction["attraction_name"],
                    "location": {
                        "latitude": attraction["location"]["latitude"],
                        "longitude": attraction["location"]["longitude"],
                    },
                    "date": attraction["date"],
                    "hour": attraction["hour"],
                }
            )

        dict_plan[day] = daily_attractions

    return {
        "user_id": plan["user_id"],
        "plan_name": plan["plan_name"],
        "destination": plan["destination"],
        "image": plan["image"],
        "init_date": str(plan["init_date"]),
        "end_date": str(plan["end_date"]),
        "attractions": plan["attractions"],
        "plan": dict_plan,
    }


def parse_plan_dto(plan: schema.Plan) -> dict:
    dict_plan = parse_plan(plan)
    dict_plan["id"] = str(plan["_id"])
    return dict_plan


def parse_plan_list(plans: list[schema.Plan]) -> list[dict]:
    return [parse_plan_dto(plan) for plan in plans]
