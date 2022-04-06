import asyncio
import argparse
import json
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT + "/..")

from src.api.schemas import FeedbackSchema
from src.db.postgres.crud import FeedbackCRUD
from src.db.postgres.db import SessionLocal


def make_parser():
    parser = argparse.ArgumentParser(description="Insert data.")
    parser.add_argument(
        "-f", dest="file", default=None, type=str, help="Input json file."
    )
    return parser


def read_from_json(file):
    with open(file, "r") as f:
        jsonContent = f.read()
        aList = json.loads(jsonContent)
    return aList


def insert_data(list_feedback: list, db=SessionLocal()):
    for item in list_feedback:
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(
            FeedbackCRUD.create_feedback(db=db, feedback=FeedbackSchema(**item))
        )


if __name__ == "__main__":
    input_json = os.path.join(PROJECT_ROOT, "feedbackList.json")

    parser = make_parser()
    args = parser.parse_args()

    if args.file:
        input_json = args.file

    feedback_list = read_from_json(input_json)
    insert_data(feedback_list)

