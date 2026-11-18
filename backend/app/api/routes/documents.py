
from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
from datetime import datetime, timezone


from app.schemas.documents import (
    DocumentResponse,
    DocumentUploadResponse,
    DocumentListResponse,
    ProcessDocumentResponse
)

router = APIRouter()

# Temporary in-memory document storage
documents_db = []


@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    document = {
        "document_id": str(uuid4()),
        "filename": file.filename,
        "content_type": file.content_type,
        "status": "uploaded",
        "uploaded_at": datetime.now(timezone.utc).isoformat()
    }

    documents_db.append(document)

    await file.close()

    return {
        "message": "Document uploaded successfully",
        "document": document
    }


@router.get("/documents", response_model=DocumentListResponse)
def get_documents():

    return {
        "total": len(documents_db),
        "documents": documents_db
    }


@router.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str):

    for document in documents_db:

        if document["document_id"] == document_id:
            return document

    raise HTTPException(
        status_code=404,
        detail="Document not found"
    )

@router.post("/documents/{document_id}/process", response_model=ProcessDocumentResponse)
def process_document(document_id: str):

    for document in documents_db:

        if document["document_id"] == document_id:

            document["status"] = "processing_requested"

            return {
                "message": "Document processing requested",
                "document_id": document_id,
                "status": document["status"]
            }

    raise HTTPException(
        status_code=404,
        detail="Document not found"
    )
