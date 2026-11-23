from fastapi import FastAPI, Request

from boe_service.agent.agent import inquire

app = FastAPI(title="BOE Service")


@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    user_message = body.get("message")
    if not user_message:
        return {"message": "Error There Is Not Message"}
    agent_answer = inquire(body["message"])
    return {"message": agent_answer}

