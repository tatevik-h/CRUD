import asyncio
import unittest
import json
from fastapi import Request as request

from fastapi.testclient import TestClient

from src.main import app
from src.models import Waiter
from src.api.schemas import FeedbackSchema
from tests.test_db import TestSessionLocal as SessionLocal
from src.db.postgres.crud import FeedbackCRUD
from tests.support import examples as data


class FeedbackCRUDTestCase(unittest.TestCase):
    def setUp(self, db=SessionLocal()):
        self.app = TestClient(app)
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

    def test_list_feedback(self, db=SessionLocal()):
        count_in_data = len(self.data)

        feedback, count = self.event_loop.run_until_complete(
            FeedbackCRUD.list_feedback(db=db)
        )

        self.assertEqual(count, count_in_data)

    def test_list_feedback_with_free_comment(self, db=SessionLocal()):
        count_in_data = sum(item.get("comment") is not None for item in self.data)

        feedback, count = self.event_loop.run_until_complete(
            FeedbackCRUD.list_feedback(db=db, has_free_comment=True)
        )

        self.assertEqual(count, count_in_data)

    def test_list_feedback_with_score_filter(self, db=SessionLocal()):
        count_in_data = sum(item.get("score") == 3 for item in self.data)

        feedback, count = self.event_loop.run_until_complete(
            FeedbackCRUD.list_feedback(db=db, score_filter=[3])
        )

        self.assertEqual(count, count_in_data)

