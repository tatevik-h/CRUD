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


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(EmailType, nullable=False)
    score = Column(Integer(), nullable=False)
    comment = Column(String)
    time_created = Column(DateTime(timezone=True), default=func.now())
    waiter_id = Column(Integer, ForeignKey("waiter.id"))
    waiter = relationship("Waiter")
