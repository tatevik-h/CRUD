from sqlalchemy.orm import Session

from src.models.waiter import Waiter


class WaiterCRUD:
    model_class = Waiter

    async def get_waiters(db: Session, skip: int = 0, limit: int = 100):
        waiters = db.query(Waiter).offset(skip).limit(limit).all()
        return waiters

