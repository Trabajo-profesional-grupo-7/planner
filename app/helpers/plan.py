from app.model.plan import Plan


def parse_plan(plan: Plan) -> dict:
    dict = {}
    dict["user_id"] = plan.user_id
    dict["plan_name"] = plan.plan_name
    dict["init_date"] = str(plan.init_date)
    dict["end_date"] = str(plan.end_date)
    plan_dict = {}

    for day in plan.plan.keys():
        attr = []
        for a in plan.plan[day]:
            attr.append(
                {
                    "attraction_id": a.attraction_id,
                    "date": str(a.date),
                    "hour": str(a.hour),
                }
            )
        plan_dict[str(day)] = attr

    dict["plan"] = plan_dict

    return dict
