import unittest
from datetime import date

from pydantic import ValidationError

import app
from app.schema.schemas import AttractionPlan


class TestAttractionPlan(unittest.TestCase):
    def test_attraction_plan_creation(self):
        attraction_plan = AttractionPlan(
            plan_id="plan_id", date="2024-07-07", attraction_id="attraction_id"
        )
        self.assertEqual(attraction_plan.plan_id, "plan_id")
        self.assertEqual(attraction_plan.date, "2024-07-07")
        self.assertEqual(attraction_plan.attraction_id, "attraction_id")

    def test_attraction_plan_validation_error(self):
        with self.assertRaises(ValidationError):
            AttractionPlan(
                plan_id=123,  # plan_id should be a string
                date="invalid_date",  # date should be a datetime
                attraction_id="attraction_id",
            )
