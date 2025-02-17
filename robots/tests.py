import json

from django.http import JsonResponse
from django.urls import reverse
from django.test import TestCase

class TestAddRobot(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data = {
            1: {"model": "R2", "version": "D2", "created": "2022-12-31 23:59:59"},
            2: {"model": "13", "version": "XS", "created": "2023-01-01 00:00:00"},
            3: {"model": "X5", "version": "LT", "created": "2023-01-01 00:00:01"},
        }
        cls.test_invalid_data = {
            1: {"model": 2, "version": "D2", "created": "2022-12-31 23:59:59"},
            2: {"model": "13", "version": "XS", "created": "2023-01-01 00:00:00"},
            3: {"model": "X5", "version": "LT", "created": "2023-01-01 00:00:01"},
        }
        super().setUpClass()

    def test_create_robot(self):
        json_data = json.dumps(self.test_data)
        response: JsonResponse = self.client.post(
            path=reverse("robots:add"),
            content_type="json",
            data=json_data
        )
        self.assertEqual(response.status_code, 200)

    def test_error_create(self):
        json_data = json.dumps(self.test_invalid_data)
        response: JsonResponse = self.client.post(
            path=reverse("robots:add"),
            content_type="json",
            data=json_data
        )
        self.assertEqual(response.status_code, 403)
