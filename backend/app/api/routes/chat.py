from fastapi import APIRouter, HTTPException

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.services.rag import generate_answer
from backend.services.document_repository import get_document

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # Step 1: Check whether the document exists
    document = get_document(request.document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    # Step 2: Check whether document processing is complete
    if document["status"] != "completed":
        raise HTTPException(
            status_code=409,
            detail=f"Document is not ready for chat. Current status: {document['status']}"
        )

    # Step 3: Generate the answer
    try:
        result = generate_answer(
            question=request.message,
            document_id=request.document_id,
        )

        return {
            "message": "Answer generated successfully",
            "question": request.message,
            "answer": result["answer"],
            "sources": result["sources"],
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to generate an answer. Please try again.",
        ) from exc