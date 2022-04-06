import asyncio
import unittest
import json

from fastapi.testclient import TestClient

from .support import converted_data as data
from src.main import app
from src.db.postgres.crud import FeedbackCRUD
from src.db.postgres.db import SessionLocal


class CreateFeedbackTestCase(unittest.TestCase):
    def setUp(self):
        self.app = TestClient(app)
        self.event_loop = asyncio.get_event_loop()
        self.test_request_payload = data.get_feedback_test_request_data()
        self.test_response_paylaod = data.get_feedback_test_response_data()

    def tearDown(self, db=SessionLocal()):
        self.event_loop.run_until_complete(
            FeedbackCRUD.delete_feedback_by_full_name(
                db=db,
                name=self.test_request_payload["full_name"]
            )
        )

    def test_create_feedback_success_case(self):
        response = self.app.post(
            "/survey/create",
            data=json.dumps(self.test_request_payload),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.test_response_paylaod)

    def test_create_feedback_failure_case(self):
        response = self.app.post(
            "/survey/create",
            data=json.dumps({"full_name": "John"}),
        )

        self.assertEqual(response.status_code, 422)

