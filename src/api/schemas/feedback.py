from typing import Optional

from pydantic import BaseModel


class Feedback(BaseModel):
    full_name: str
    phone_number: str
    email: str
    score: int
    comment: Optional[str] = None
    waiter_name: Optional[str] = None

    class Config:
        orm_mode = True
