# chat_router.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

# Import your send_message function from wherever it lives
from src.boe_service.agent.agent import send_message
from src.boe_service.api.crud import (
    ChatRequest,
    ChatResponse,
    create_chat,
    fetch_all_chats,
    fetch_chat_by_id,
)
from src.boe_service.pg_db import get_db

# Create the router
chat_router = APIRouter(prefix="/chats", tags=["Messages"])

SessionDep = Annotated[Session, Depends(get_db)]


# Update Chat - To Be Updated
@chat_router.post("/chat")
async def chat(req: Request):
    body = await req.json()
    user_message = body.get("message")
    if not user_message:
        return {"message": "Error There Is Not Message"}

    agent_answer = send_message(user_message)
    return {"message": agent_answer}


# Get All Chats
@chat_router.get("/")
def get_all_chats_api(session: SessionDep):
    all_chats = fetch_all_chats(session)
    return all_chats


@chat_router.get("/{chat_id}")
def get_chat_by_id(chat_id: int, session: SessionDep):
    chat = fetch_chat_by_id(session, chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@chat_router.post("/", response_model=ChatResponse)
def post_chat(data: ChatRequest, session: SessionDep):
    chat = create_chat(session, data)
    return chat


@chat_router.delete("/{chat_id}")
def delete_chat(chat_id: int, session: SessionDep):
    pass
