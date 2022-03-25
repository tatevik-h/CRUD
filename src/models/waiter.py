from sqlalchemy import (
    Column, 
    String, 
    Integer, 
    DateTime, 
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType

from src.db.postgres.db import Base


class Waiter(Base):
    __tablename__ = "waiter"

    id = Column(Integer, primary_key=True)
    name = Column(String)

