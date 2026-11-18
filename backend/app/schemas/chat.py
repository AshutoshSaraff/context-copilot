
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Question asked by the user"
    )


class ChatResponse(BaseModel):
    message: str
    question: str
    answer: str
