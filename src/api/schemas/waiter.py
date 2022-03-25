from typing import Optional

from pydantic import BaseModel


class Waiter(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True

