from datetime import date, timedelta
from typing import Dict, List, Optional

from pydantic import BaseModel


class Location(BaseModel):
    latitude: float
    longitude: float


class Attraction(BaseModel):
    attraction_id: str
    attraction_name: str
    location: Location
    date: str
    hour: Optional[timedelta] = None


class PlanMetadata(BaseModel):
    user_id: int
    plan_name: str
    destination: str
    init_date: date
    end_date: date


class Plan(PlanMetadata):
    plan: Dict[str, List[Attraction]]
