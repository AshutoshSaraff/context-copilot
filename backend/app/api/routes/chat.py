
from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return {
        "message": "Chat request received successfully",
        "question": request.message,
        "answer": "Chat functionality is under development."
    }
