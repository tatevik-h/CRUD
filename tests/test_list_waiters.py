import asyncio
import unittest
import json

from fastapi.testclient import TestClient

from src.main import app


class CreateFeedbackTestCase(unittest.TestCase):
    def setUp(self):
        self.app = TestClient(app)

    def tearDown(self):
        pass

    def test_list_waiters_success_case(self):
        test_data = []

        response = self.app.get("survey/waiter")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_data)

