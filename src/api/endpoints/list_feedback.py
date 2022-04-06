from typing import List, Union

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Request,
    Query,
)
from sqlalchemy.orm import Session

from src.api.schemas import FeedbackSchema
from src.db.postgres.crud import FeedbackCRUD
from src.db.postgres.db import engine, get_db
from src.models import feedback as models
from utils.restful import Paginator


router = APIRouter()


@router.get("/list-feedback")
async def list_feedback(
    request: Request,
    page: int = Query(Paginator.DEFAULT_PAGE, gt=0),
    per_page: int = Query(Paginator.DEFAULT_PAGE_SIZE, gt=0, le=50),
    score_filter: List[int] = Query([1, 2, 3, 4, 5]),
    has_free_comment: bool = Query(None),
    db: Session = Depends(get_db),
) -> dict:
    paginator = Paginator(request=request)
    feedback, count = await FeedbackCRUD.list_feedback(
        db=db,
        score_filter=score_filter,
        has_free_comment=has_free_comment,
    )

    return await paginator.paginate(
        page=page,
        per_page=per_page,
        query_model=feedback,
        document_count=count,
        collection_name="feedback_list",
    )
