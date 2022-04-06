import asyncio
import unittest
import json
from fastapi import Request as request

from fastapi.testclient import TestClient

from src.models import Waiter
from src.api.schemas import WaiterSchema
from tests.test_db import TestSessionLocal as SessionLocal

# from src.db.postgres.db import SessionLocal
from src.db.postgres.crud import WaiterCRUD
from tests.support import examples as data


class WaiterCRUDTestCase(unittest.TestCase):
    def setUp(self, db=SessionLocal()):
        self.data = data.get_waiter_data()
        self.filled_waiters = data.get_waiter_responce_data()
        self.event_loop = asyncio.get_event_loop()

        for item in self.data:
            db_waiter = Waiter(name=item["name"], id=item["id"])
            db.add(db_waiter)
            db.commit()

    def tearDown(self, db=SessionLocal()):
        for item in self.data:
            waiter = db.query(Waiter).filter_by(name=item["name"]).first()
            db.delete(waiter)
            db.commit()

    def test_get_waiters(self, db=SessionLocal()):
        waiters = self.event_loop.run_until_complete(WaiterCRUD.get_waiters(db=db))

        self.assertEqual(len(waiters), len(self.filled_waiters))

