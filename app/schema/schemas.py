from app.model.plan import Plan


def individual_serial(plan) -> Plan:
    return {
        "id": str(plan["_id"]),
        "plan_name": plan["plan_name"],
        "init_date": plan["init_date"],
        "end_date": plan["end_date"],
        "plan": plan["plan"],
    }


def list_serial(plans) -> list:
    return [individual_serial(plan) for plan in plans]
