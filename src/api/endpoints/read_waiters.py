from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from src.api.schemas import WaiterSchema
from src.db.postgres.crud import WaiterCRUD
from src.db.postgres.db import engine, get_db
from src.models import feedback as models
 
models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/survey/waiter", response_model=List[WaiterSchema])
async def list_waiters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    waiters = await WaiterCRUD.get_waiters(db, skip=skip, limit=limit)
    return waiters

