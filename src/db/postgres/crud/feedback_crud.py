from sqlalchemy.orm import Session

from src.api.schemas import FeedbackSchema
from src.models.feedback import Feedback
from src.models.waiter import Waiter


class FeedbackCRUD:
    model_feedback_class = Feedback
    model_waiter_class = Waiter

    @classmethod
    async def create_feedback(cls, db: Session, feedback: FeedbackSchema):
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

    @classmethod
    async def delete_feedback_by_full_name(cls, db: Session, name: str):
        feedback = db.query(Feedback).filter_by(full_name=name).first()
        db.delete(feedback)
        db.commit()

    @classmethod
    async def list_feedback(cls, db: Session, score_filter=None, has_free_comment=None):
        #feedback_cursor = db.query(
        #    cls.model_feedback_class.full_name,
        #    cls.model_feedback_class.phone_number,
        #    cls.model_feedback_class.email,
        #    cls.model_feedback_class.time_created,
        #    cls.model_feedback_class.comment,
        #    cls.model_feedback_class.score,
        #    cls.model_feedback_class.waiter_id,
        #    cls.model_waiter_class.name.label("waiter_name"),
        #).join(
        #    cls.model_waiter_class,
        #    cls.model_feedback_class.waiter_id == cls.model_waiter_class.id,
        #    isouter=True,
        #)
        feedback_cursor = db.query(cls.model_feedback_class)

        if score_filter:
            feedback_cursor = feedback_cursor.filter(
                cls.model_feedback_class.score.in_(score_filter)
            )

        if has_free_comment:
            feedback_cursor = feedback_cursor.filter(
                cls.model_feedback_class.comment != None
            )

        #feedback_cursor = db.query(
        #        .waiter
        #        )

        feedback_count = feedback_cursor.count()

        return feedback_cursor, feedback_count
