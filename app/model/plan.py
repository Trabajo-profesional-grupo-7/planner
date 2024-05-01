from datetime import date, timedelta
from typing import Dict, List

from pydantic import BaseModel


class Location(BaseModel):
    latitude: float
    longitude: float


class Attraction(BaseModel):
    attraction_id: str
    location: Location
    date: date
    hour: timedelta


class PlanMetadata(BaseModel):
    user_id: int
    plan_name: str
    destination: str
    init_date: date
    end_date: date


class Plan(PlanMetadata):
    plan: Dict[date, List[Attraction]]
