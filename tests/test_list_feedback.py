import asyncio
import unittest
import json
from fastapi import Request as request

from fastapi.testclient import TestClient

from src.main import app
from src.api.schemas import FeedbackSchema
from src.models import Waiter

from tests.test_db import TestSessionLocal as SessionLocal, client
from src.db.postgres.crud import FeedbackCRUD
from tests.support import examples as data


class ListFeedbackTestCase(unittest.TestCase):
    def setUp(self, db=SessionLocal()):
        self.app = client
        self.data = data.get_feedback_data()
        self.waiter_data = data.get_waiter_data()
        self.created_feedback = []
        self.event_loop = asyncio.get_event_loop()

        for item in self.waiter_data:
            db_waiter = Waiter(name=item["name"], id=item["id"])
            db.add(db_waiter)
            db.commit()

        for item in self.data:
            self.created_feedback.append(
                self.event_loop.run_until_complete(
                    FeedbackCRUD.create_feedback(db=db, feedback=FeedbackSchema(**item))
                )
            )

    def tearDown(self, db=SessionLocal()):
        for item in self.created_feedback:
            self.event_loop.run_until_complete(
                FeedbackCRUD.delete_feedback_by_full_name(db=db, name=item.full_name)
            )

        for item in self.waiter_data:
            waiter = db.query(Waiter).filter_by(name=item["name"]).first()
            db.delete(waiter)
            db.commit()

    def test_list_feedback_success_case(self):
        response = self.app.get("/list-feedback?page=1&per_page=5")
        self.assertEqual(response.status_code, 200)

    def test_list_feedback_failure_case(self):
        response = self.app.get("/list-feedback?has_free_comment=aaa")
        self.assertEqual(response.status_code, 422)

        response = self.app.get("/list-feedback?score_filter=score")
        self.assertEqual(response.status_code, 422)

