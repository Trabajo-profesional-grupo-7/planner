from typing import List

from pydantic import BaseModel


class Place(BaseModel):
    attraction_id: str
    attraction_name: str


class Places(BaseModel):
    places: List[Place]
    total: int
