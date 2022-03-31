from sqlalchemy.orm import Session

from src.api.schemas import FeedbackSchema
from src.models.feedback import Feedback


class FeedbackCRUD:
    model_class = Feedback

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

