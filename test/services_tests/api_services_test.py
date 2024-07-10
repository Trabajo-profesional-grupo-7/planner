import os
import unittest
from unittest.mock import Mock, patch

import requests

import app
from app.services.api import *


class TestGetUserPreferences(unittest.TestCase):

    @patch("app.services.api.requests.get")
    def test_get_user_preferences(self, mock_get):
        mock_response = Mock()
        expected_data = ["Museum", "Park", "Cafe"]
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        user_id = 1
        result = get_user_preferences(user_id)
        self.assertEqual(result, expected_data)

    @patch("app.services.api.requests.get")
    def test_get_user_preferences_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException

        user_id = 1
        with self.assertRaises(requests.exceptions.RequestException):
            get_user_preferences(user_id)


class TestGetNearbyAttractions(unittest.TestCase):
    @patch("app.services.api.requests.post")
    def test_get_nearby_attractions(self, mock_post):
        mock_response = Mock()
        expected_data = [
            {
                "attraction_id": "ChIJIxYSMMbKvJURqZGJyCpvOFM",
                "attraction_name": "Teatro Colón",
                "city": "Buenos Aires",
                "country": "Argentina",
                "location": {"latitude": -34.6011105, "longitude": -58.3835359},
                "photo": "https://places.googleapis.com/v1/places/ChIJIxYSMMbKvJURqZGJyCpvOFM/photos/AUGGfZmrXWLEBJwjH5x41ugoVBWMwvpCyrx4Gkky8lHykLq1fSqS9JbdRsXrBcS5EIBhAKIREofrridIiaRXDRPHpBgT2hie8yatBu43e9pQe06vxNcuYQ3MKQvF0i5-VLXzlT_1CNgEr-RYhv6gPVgXLdDdCD7HIec2LLo9/media?maxHeightPx=400&maxWidthPx=400&key=AIzaSyANHkik_wSkYoNNsExts3-TtZCM2fMb5R8",
                "avg_rating": 4.8,
                "liked_count": 0,
                "types": [
                    "performing_arts_theater",
                    "tourist_attraction",
                    "event_venue",
                ],
                "formatted_address": "Tucumán 1171, C1049 Cdad. Autónoma de Buenos Aires, Argentina",
                "google_maps_uri": "https://maps.google.com/?cid=5996665133387583913",
                "editorial_summary": "This grand theater (circa 1908) known for acoustics hosts classical music, operas, ballets & tours.",
            },
            {
                "attraction_id": "ChIJm86rLcTKvJURjRPk21bRoro",
                "attraction_name": "Pizzería Güerrín",
                "city": "Buenos Aires",
                "country": "Argentina",
                "location": {"latitude": -34.6041209, "longitude": -58.385982},
                "photo": "https://places.googleapis.com/v1/places/ChIJm86rLcTKvJURjRPk21bRoro/photos/AUc7tXWQ3q8lOSo4e1-G5rfJSnRG-CLnE7Rh9uocc_bsRxxzrw2voQQKIc-Pp4dFj9Fa1GEwNbsPZZzeGfqdUIHFcBKkIT_pQJU9mRfCzbQZwndKtNQmqbzsv51Cv1ZiZI0l8QOyV1kxIJKKmT3o8lE9U7663tEHzOjca9qw/media?maxHeightPx=400&maxWidthPx=400&key=AIzaSyANHkik_wSkYoNNsExts3-TtZCM2fMb5R8",
                "avg_rating": 4.6,
                "liked_count": 0,
                "types": ["pizza_restaurant", "fast_food_restaurant", "restaurant"],
                "formatted_address": "Av. Corrientes 1368, C1043 Cdad. Autónoma de Buenos Aires, Argentina",
                "google_maps_uri": "https://maps.google.com/?cid=13448541608268272525",
                "editorial_summary": "Hopping institution for traditional Argentinian-style pizza & empanadas, open since 1932.",
            },
        ]
        mock_response.json.return_value = expected_data
        mock_post.return_value = mock_response

        user_preferences = ["museum", "park"]
        latitude = -34.601
        longitude = -58.383
        radius = 50000

        result = get_nearby_attractions(user_preferences, latitude, longitude, radius)
        self.assertEqual(result, expected_data)

    @patch("app.services.api.requests.post")
    def test_get_nearby_attractions_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException

        user_preferences = ["museum", "park"]
        latitude = -34.601
        longitude = -58.383
        radius = 1000

        with self.assertRaises(requests.exceptions.RequestException):
            get_nearby_attractions(user_preferences, latitude, longitude, radius)


class TestGetRecommendedAttractions(unittest.TestCase):
    @patch("app.services.api.requests.post")
    def test_get_recommended_attractions(self, mock_post):
        mock_response = Mock()
        expected_data = [
            {
                "attraction_id": "ChIJIxYSMMbKvJURqZGJyCpvOFM",
                "attraction_name": "Teatro Colón",
                "city": "Buenos Aires",
                "country": "Argentina",
                "location": {"latitude": -34.6011105, "longitude": -58.3835359},
                "photo": "https://places.googleapis.com/v1/places/ChIJIxYSMMbKvJURqZGJyCpvOFM/photos/AUGGfZmrXWLEBJwjH5x41ugoVBWMwvpCyrx4Gkky8lHykLq1fSqS9JbdRsXrBcS5EIBhAKIREofrridIiaRXDRPHpBgT2hie8yatBu43e9pQe06vxNcuYQ3MKQvF0i5-VLXzlT_1CNgEr-RYhv6gPVgXLdDdCD7HIec2LLo9/media?maxHeightPx=400&maxWidthPx=400&key=AIzaSyANHkik_wSkYoNNsExts3-TtZCM2fMb5R8",
                "avg_rating": 4.8,
                "liked_count": 0,
                "types": [
                    "performing_arts_theater",
                    "tourist_attraction",
                    "event_venue",
                ],
                "formatted_address": "Tucumán 1171, C1049 Cdad. Autónoma de Buenos Aires, Argentina",
                "google_maps_uri": "https://maps.google.com/?cid=5996665133387583913",
                "editorial_summary": "This grand theater (circa 1908) known for acoustics hosts classical music, operas, ballets & tours.",
            },
            {
                "attraction_id": "ChIJm86rLcTKvJURjRPk21bRoro",
                "attraction_name": "Pizzería Güerrín",
                "city": "Buenos Aires",
                "country": "Argentina",
                "location": {"latitude": -34.6041209, "longitude": -58.385982},
                "photo": "https://places.googleapis.com/v1/places/ChIJm86rLcTKvJURjRPk21bRoro/photos/AUc7tXWQ3q8lOSo4e1-G5rfJSnRG-CLnE7Rh9uocc_bsRxxzrw2voQQKIc-Pp4dFj9Fa1GEwNbsPZZzeGfqdUIHFcBKkIT_pQJU9mRfCzbQZwndKtNQmqbzsv51Cv1ZiZI0l8QOyV1kxIJKKmT3o8lE9U7663tEHzOjca9qw/media?maxHeightPx=400&maxWidthPx=400&key=AIzaSyANHkik_wSkYoNNsExts3-TtZCM2fMb5R8",
                "avg_rating": 4.6,
                "liked_count": 0,
                "types": ["pizza_restaurant", "fast_food_restaurant", "restaurant"],
                "formatted_address": "Av. Corrientes 1368, C1043 Cdad. Autónoma de Buenos Aires, Argentina",
                "google_maps_uri": "https://maps.google.com/?cid=13448541608268272525",
                "editorial_summary": "Hopping institution for traditional Argentinian-style pizza & empanadas, open since 1932.",
            },
        ]
        mock_response.json.return_value = expected_data
        mock_post.return_value = mock_response

        user_id = 1
        destination = "Buenos Aires"
        user_preferences = ["museum", "park"]

        result = get_recommended_attractions(user_id, destination, user_preferences)
        self.assertEqual(result, expected_data)

    @patch("app.services.api.requests.post")
    def test_get_recommended_attractions_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException

        user_id = 1
        destination = "Buenos Aires"
        user_preferences = ["museum", "park"]

        with self.assertRaises(requests.exceptions.RequestException):
            get_recommended_attractions(user_id, destination, user_preferences)
