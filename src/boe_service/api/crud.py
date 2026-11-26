# crud.py
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.boe_service.api.models.models import Chat, User


class ChatRequest(BaseModel):
    user_id: int
    title: str | None = None


class ChatResponse(BaseModel):  # what the API sends back
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    title: str


def fetch_all_chats(session: Session):
    smt = select(Chat)
    return session.scalars(smt).all()


def fetch_chat_by_id(session: Session, chat_id: int):
    smt = select(Chat).where(Chat.id == chat_id)
    return session.scalars(smt).one_or_none()


def create_chat(session: Session, data: ChatRequest):
    if session.get(User, data.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    chat = Chat(user_id=data.user_id)
    if data.title:
        chat.title = data.title
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat
