from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from agent import chat


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        response = chat(
            request.message,
            request.session_id
        )

        return {
            "response": response
        }

    except Exception:
        return {
            "response": "Sorry, something went wrong. Please try again or contact a human support agent."
        }