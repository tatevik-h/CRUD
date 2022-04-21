import asyncio

from sqlalchemy.orm import Session

from ..filters import FilterQueryBuilder
from src.api.schemas import FeedbackSchema
from src.models.feedback import Feedback
from src.models.waiter import Waiter


class FeedbackCRUD:
    model_feedback_class = Feedback
    model_waiter_class = Waiter

    @staticmethod
    async def create_feedback(db: Session, feedback: FeedbackSchema) -> object:
        db_feedback = Feedback(
            full_name=feedback.full_name,
            phone_number=feedback.phone_number,
            email=feedback.email,
            score=feedback.score,
            comment=feedback.comment,
            waiter_id=feedback.waiter_id,
        )
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        return db_feedback

    @staticmethod
    def get_feedback_by_full_name(db: Session, name: str):
        feedback = db.query(Feedback).filter_by(full_name=name).first()
        return feedback

    @staticmethod
    async def delete_feedback_by_full_name(db: Session, name: str):
        feedback = FeedbackCRUD.get_feedback_by_full_name(db=db, name=name)
        if feedback:
            db.delete(feedback)
            db.commit()

    @classmethod
    async def list_feedback(
        cls,
        db: Session,
        score_filter=None,
        has_free_comment=None,
    ):
        feedback_query = []
        if score_filter or has_free_comment:
            feedback_query = FilterQueryBuilder.create(
                    [has_free_comment, score_filter]
            )

        feedback = (
            db.query(cls.model_feedback_class)
            .filter(*feedback_query)
            .order_by(cls.model_feedback_class.time_created.desc())
        )

        feedback_count = feedback.count()

        return feedback, feedback_count
