from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from src.api.schemas import FeedbackSchema
from src.db.postgres.crud import FeedbackCRUD
from src.db.postgres.db import engine, get_db
from src.models import feedback as models
 
models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/survey/create", response_model=FeedbackSchema)
async def create_feedback(feedback: FeedbackSchema, db: Session = Depends(get_db)):
    return await FeedbackCRUD.create_feedback(db=db, feedback=feedback)

