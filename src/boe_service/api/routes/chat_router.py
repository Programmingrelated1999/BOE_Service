# chat_router.py
from fastapi import APIRouter, Request

# Import your send_message function from wherever it lives
from boe_service.agent.agent import send_message

# 1. Create the router
chat_router = APIRouter()


# 2. Use @router.post instead of @app.post
@chat_router.post("/chat")
async def chat(req: Request):
    body = await req.json()
    user_message = body.get("message")
    if not user_message:
        return {"message": "Error There Is Not Message"}

    agent_answer = send_message(user_message)
    return {"message": agent_answer}
