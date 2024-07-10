import unittest
from datetime import date

from pydantic import ValidationError

import app
from app.schema.schemas import Plan, PlanMetadata


class TestPlanMetadata(unittest.TestCase):
    def test_plan_metadata_creation(self):
        metadata = PlanMetadata(
            user_id=1,
            plan_name="Summer Vacation",
            destination="Cordoba",
            init_date=date(2024, 12, 20),
            end_date=date(2024, 12, 26),
        )
        self.assertEqual(metadata.user_id, 1)
        self.assertEqual(metadata.plan_name, "Summer Vacation")
        self.assertEqual(metadata.destination, "Cordoba")
        self.assertEqual(metadata.init_date, date(2024, 12, 20))
        self.assertEqual(metadata.end_date, date(2024, 12, 26))

    def test_plan_metadata_validation_error(self):
        with self.assertRaises(ValidationError):
            PlanMetadata(
                user_id="user_id",  # user id should be int
                plan_name="Summer Vacation",
                destination="Cordoba",
                init_date="2024-12-20",  # init date should be a datetime
                end_date="2024-12-26",  # end date should be datetime
            )


class TestPlan(unittest.TestCase):
    def test_plan_creation(self):
        plan = Plan(id="plan_id")
        self.assertEqual(plan.id, "plan_id")

    def test_plan_validation_error(self):
        with self.assertRaises(ValidationError):
            Plan(id=1)  # id should be a string
