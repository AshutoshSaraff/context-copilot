
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Question asked by the user",
    )
    document_id: str = Field(
        ...,
        min_length=1,
        description="ID of the uploaded document",
    )


class SourceResponse(BaseModel):
    chunk_id: str
    page_number: int | None = None
    distance: float
    text: str


class ChatResponse(BaseModel):
    message: str
    question: str
    answer: str
    sources: list[SourceResponse]
