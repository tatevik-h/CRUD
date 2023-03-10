from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.api.endpoints import (
    create_feedback,
    read_waiters,
    list_feedback,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(create_feedback.router)
app.include_router(read_waiters.router)
app.include_router(list_feedback.router)
