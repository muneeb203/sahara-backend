"""FastAPI wrapper for deploying HerHaq chatbot on Render."""

import os
import sys
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from chatbot import HerHaqChatbot  # noqa: E402
from utils import load_config, setup_logging  # noqa: E402


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    message: str = Field(..., min_length=1, description="User message text")
    session_id: Optional[str] = Field(
        default="default",
        description="Client-managed session ID for conversation continuity",
    )


class ChatResponse(BaseModel):
    """API response for chat endpoint."""

    response: str
    sources: List[Dict[str, Any]]
    is_safety_response: bool
    session_id: str


app = FastAPI(title="HerHaq Chatbot API", version="1.0.0")

# Global chatbot singleton + session history map.
chatbot: Optional[HerHaqChatbot] = None
session_histories: Dict[str, List[Dict[str, Any]]] = {}
chatbot_lock = threading.Lock()


def _parse_cors_origins() -> List[str]:
    """Read CORS origins from env; fallback to wildcard."""
    env_value = os.getenv("CORS_ORIGINS", "*").strip()
    if env_value == "*":
        return ["*"]
    return [origin.strip() for origin in env_value.split(",") if origin.strip()]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    """Initialize chatbot once at startup."""
    global chatbot

    setup_logging()
    config = load_config()
    chatbot = HerHaqChatbot(config)


@app.get("/")
def root() -> Dict[str, str]:
    """Simple root endpoint."""
    return {"message": "HerHaq API is running"}


@app.get("/health")
def health() -> Dict[str, str]:
    """Health endpoint for uptime checks."""
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Handle chatbot query via API."""
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")

    session_id = (request.session_id or "default").strip() or "default"
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        with chatbot_lock:
            chatbot.conversation_history = session_histories.get(session_id, []).copy()
            result = chatbot.chat(message)
            session_histories[session_id] = chatbot.get_conversation_history().copy()

        return ChatResponse(
            response=result["response"],
            sources=result.get("sources", []),
            is_safety_response=result.get("is_safety_response", False),
            session_id=session_id,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
