import asyncio
import unittest
import json

from fastapi.testclient import TestClient

from src.main import app
from tests.test_db import TestSessionLocal as SessionLocal, client
from src.models import Waiter

from tests.support import examples as data


class CreateFeedbackTestCase(unittest.TestCase):
    def setUp(self, db=SessionLocal()):
        self.app = client
        self.test_response_payload = data.get_waiter_responce_data()
        self.waiter_data = data.get_waiter_data()

        for item in self.waiter_data:
            db_waiter = Waiter(name=item["name"], id=item["id"])
            db.add(db_waiter)
            db.commit()

    def tearDown(self, db=SessionLocal()):
        for item in self.waiter_data:
            waiter = db.query(Waiter).filter_by(name=item["name"]).first()
            db.delete(waiter)
            db.commit()

    def test_list_waiters_success_case(self):
        test_data = self.test_response_payload

        response = self.app.get("survey/waiter")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_data)
        
