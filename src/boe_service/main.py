import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text

from boe_service.agent.agent import send_message

app = FastAPI(title="BOE Service")

load_dotenv()
DATABASE_URL = f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL, echo=True)

with engine.connect() as conn:
    print(conn.execute(text("SELECT version();")).scalar())


@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    user_message = body.get("message")
    if not user_message:
        return {"message": "Error There Is Not Message"}
    agent_answer = send_message(body["message"])
    return {"message": agent_answer}
