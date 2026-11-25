import enum
from datetime import datetime

from sqlalchemy import Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from boe_service.pg_db import Base


class Sender(enum.Enum):
    ASSISTANT = "assistant"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(50), unique=True)


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(50), default="Conversation Placeholder")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender: Mapped[Sender] = mapped_column(
        Enum(Sender, values_callable=lambda e: [m.value for m in e])
    )
    text: Mapped[str] = mapped_column(Text)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
