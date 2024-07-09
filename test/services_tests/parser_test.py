import unittest
from datetime import date, timedelta
from typing import Dict, List
from unittest.mock import Mock, patch

import app
from app.model.plan import *
from app.schema.parser import parse_plan, parse_plan_list


class TestParsePlan(unittest.TestCase):
    def test_parse_plan(self):
        plan_dict = {
            "user_id": 1,
            "plan_name": "Summer plan",
            "destination": "Salta",
            "image": "http://example.com/salta_la_linda.jpg",
            "init_date": date(2024, 1, 1),
            "end_date": date(2024, 1, 3),
            "attractions": ["1", "2"],
            "plan": {
                "2024-01-01": [
                    {
                        "attraction_id": "1",
                        "attraction_name": "Attraction 1",
                        "location": {"latitude": 24.4333, "longitude": -43.2332},
                        "date": "2024-01-01",
                        "hour": timedelta(hours=1),
                    }
                ],
                "2024-01-02": [
                    {
                        "attraction_id": "2",
                        "attraction_name": "Attraction 2",
                        "location": {"latitude": 25.4433, "longitude": -43.3332},
                        "date": "2024-01-02",
                        "hour": timedelta(hours=2),
                    }
                ],
            },
        }

        result = parse_plan(plan_dict)

        expected = {
            "user_id": 1,
            "plan_name": "Summer plan",
            "destination": "Salta",
            "image": "http://example.com/salta_la_linda.jpg",
            "init_date": "2024-01-01",
            "end_date": "2024-01-03",
            "attractions": ["1", "2"],
            "plan": {
                "2024-01-01": [
                    {
                        "attraction_id": "1",
                        "attraction_name": "Attraction 1",
                        "location": {"latitude": 24.4333, "longitude": -43.2332},
                        "date": "2024-01-01",
                        "hour": timedelta(hours=1),
                    }
                ],
                "2024-01-02": [
                    {
                        "attraction_id": "2",
                        "attraction_name": "Attraction 2",
                        "location": {"latitude": 25.4433, "longitude": -43.3332},
                        "date": "2024-01-02",
                        "hour": timedelta(hours=2),
                    }
                ],
            },
        }

        self.assertEqual(result, expected)
