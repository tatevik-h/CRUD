from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    full_name: str
    phone_number: str
    email: str
    score: int
    comment: Optional[str] = None
    waiter_id: Optional[int] = None

    class Config:
        orm_mode = True


class FeedbackRetrieve(BaseModel):
    full_name: str
    phone_number: str
    email: str
    score: int
    comment: Optional[str] = None
    waiter_name: Optional[str] = None
    time_created: Optional[datetime] = None

    class Config:
        orm_mode = True
