from fastapi import FastAPI
import uvicorn

from src.api.endpoints import create_feedback, read_waiters

app = FastAPI()
app.include_router(create_feedback.router)
app.include_router(read_waiters.router)

