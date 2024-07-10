import math
import unittest
from datetime import date, timedelta
from unittest.mock import Mock

import app
from app.model.plan import Attraction, Location
from app.schema.schemas import *
from app.services.helpers import calc_distance, calc_plan_metadata, remove_attraction


class TestCalcPlanMetadata(unittest.TestCase):
    def test_calc_plan_metadata_multiple_days(self):
        plan_metadata = PlanMetadata(
            user_id=1,
            plan_name="Plan 1",
            destination="Cordoba",
            init_date=date(2024, 7, 1),
            end_date=date(2024, 7, 4),
        )
        attractions = [
            Attraction(
                attraction_id="1",
                attraction_name="Attraction 1",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-01",
            ),
            Attraction(
                attraction_id="2",
                attraction_name="Attraction 2",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-02",
            ),
            Attraction(
                attraction_id="3",
                attraction_name="Attraction 3",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-03",
            ),
            Attraction(
                attraction_id="4",
                attraction_name="Attraction 4",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-04",
            ),
            Attraction(
                attraction_id="5",
                attraction_name="Attraction 5",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-05",
            ),
            Attraction(
                attraction_id="6",
                attraction_name="Attraction 6",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-05",
            ),
        ]
        user_preferences = ["museum", "park"]

        attractions_per_day, max_type_amount = calc_plan_metadata(
            plan_metadata, attractions, user_preferences
        )

        self.assertEqual(attractions_per_day, 2)
        self.assertEqual(max_type_amount, 3)

    def test_calc_plan_metadata_max_3_attractions_per_day(self):
        plan_metadata = PlanMetadata(
            user_id=1,
            plan_name="Plan 3",
            destination="Salta",
            init_date=date(2024, 7, 1),
            end_date=date(2024, 7, 3),
        )
        attractions = [
            Attraction(
                attraction_id="1",
                attraction_name="Attraction 1",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-01",
            ),
            Attraction(
                attraction_id="2",
                attraction_name="Attraction 2",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-01",
            ),
            Attraction(
                attraction_id="3",
                attraction_name="Attraction 3",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-02",
            ),
            Attraction(
                attraction_id="4",
                attraction_name="Attraction 4",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-02",
            ),
            Attraction(
                attraction_id="5",
                attraction_name="Attraction 5",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-03",
            ),
            Attraction(
                attraction_id="6",
                attraction_name="Attraction 6",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-03",
            ),
            Attraction(
                attraction_id="7",
                attraction_name="Attraction 7",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-03",
            ),
            Attraction(
                attraction_id="8",
                attraction_name="Attraction 8",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-03",
            ),
            Attraction(
                attraction_id="9",
                attraction_name="Attraction 9",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-03",
            ),
            Attraction(
                attraction_id="10",
                attraction_name="Attraction 10",
                location=Location(latitude=23.554, longitude=-35.444),
                date="2024-07-03",
            ),
        ]
        user_preferences = ["museum", "park"]

        attractions_per_day, max_type_amount = calc_plan_metadata(
            plan_metadata, attractions, user_preferences
        )

        self.assertEqual(attractions_per_day, 3)
        self.assertEqual(max_type_amount, 3)


class TestCalcDistance(unittest.TestCase):
    def test_calc_distance_same_location(self):
        attraction_i = attraction_i = {
            "location": {"latitude": 23.554, "longitude": -35.444}
        }
        attraction_j = {"location": {"latitude": 23.554, "longitude": -35.444}}

        distance = calc_distance(attraction_i, attraction_j)

        self.assertEqual(distance, 0.0)

    def test_calc_distance_different_locations(self):
        attraction_i = {"location": {"latitude": 23.554, "longitude": -35.444}}
        attraction_j = {"location": {"latitude": 15.0, "longitude": 25.0}}

        distance = calc_distance(attraction_i, attraction_j)

        expected_distance = math.sqrt((15.0 - 23.554) ** 2 + (25.0 - -35.444) ** 2)
        self.assertAlmostEqual(distance, expected_distance, places=6)
