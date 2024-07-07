from datetime import date

from pydantic import BaseModel

from app.model import plan as model


class PlanMetadata(BaseModel):
    user_id: int
    plan_name: str
    destination: str
    init_date: date
    end_date: date


class Plan(model.Plan):
    id: str


class AttractionPlan(BaseModel):
    plan_id: str
    date: str
    attraction_id: str
