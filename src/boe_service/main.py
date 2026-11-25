from contextlib import asynccontextmanager

import models  # noqa: F401
from fastapi import FastAPI

from boe_service.api.routes.chat_router import chat_router
from pg_data import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


# Create A LifeSpan
app = FastAPI(title="BOE Service", lifespan=lifespan)
app.include_router(chat_router)
