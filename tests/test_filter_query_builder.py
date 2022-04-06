import asyncio
import unittest
import json

from fastapi.testclient import TestClient

from src.db.postgres.filters import FilterQueryBuilder
from src.models import Feedback


class FilterQueryBuilderTestCase(unittest.TestCase):
    def test_filter_query_builder(self):
        return_payload = []
        return_data = FilterQueryBuilder.create()

        self.assertEqual(return_data, return_payload)

    def test_filter_query_builder_with_bool_filter(self):
        return_payload = [Feedback.comment != None]
        return_data = FilterQueryBuilder.create(filters=[True])
        self.assertTrue(return_data[0].compare(return_payload[0]))

    def test_filter_query_builder_with_list_filter(self):
        return_payload = [Feedback.score.in_([1, 2, 3, 4])]
        return_data = FilterQueryBuilder.create(filters=[[1, 2, 3, 4]])
        self.assertTrue(return_payload[0].compare(return_data[0]))

    def test_filter_query_builder_with_both_filters(self):
        return_payload = [
            Feedback.score.in_([1, 2, 3, 4]), 
            Feedback.comment != None
        ]
        return_data = FilterQueryBuilder.create(filters=[[1, 2, 3, 4], True])
        self.assertTrue(return_payload[0].compare(return_data[0]))
        self.assertTrue(return_payload[1].compare(return_data[1]))
