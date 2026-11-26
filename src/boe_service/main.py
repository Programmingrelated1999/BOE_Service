from contextlib import asynccontextmanager

from fastapi import FastAPI

import src.boe_service.api.models.models  # noqa: F401
from boe_service.api.routes.chats_router import chat_router
from boe_service.pg_db import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create Tables
    Base.metadata.create_all(bind=engine)
    yield


# Create A LifeSpan
app = FastAPI(title="BOE Service", lifespan=lifespan)
app.include_router(chat_router)
