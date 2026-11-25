
import logging
logger = logging.getLogger(__name__)
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.app.schemas.documents import (
    DocumentResponse,
    DocumentUploadResponse,
    DocumentListResponse,
    ProcessDocumentResponse,
)

from backend.services.ingestion import ingest_document

from backend.services.document_repository import (
    create_document,
    get_document,
    get_all_documents,
    update_document_status,
)

from backend.app.schemas.documents import DeleteDocumentResponse
from backend.services.document_repository import delete_document
from backend.services.vector_store import delete_document_chunks


router = APIRouter()

# Uploaded PDFs are stored under backend/storage/uploads.
UPLOAD_DIR = (
    Path(__file__).resolve().parents[3]
    / "storage"
    / "uploads"
)

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post(
    "/documents/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(file: UploadFile = File(...)):

    try:
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )

        pdf_bytes = await file.read(MAX_UPLOAD_SIZE + 1)

        if not pdf_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty.",
            )

        if len(pdf_bytes) > MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF exceeds the 10 MB upload limit.",
            )

        if not pdf_bytes.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file.",
            )

        document_id = str(uuid4())

        file_path = UPLOAD_DIR / f"{document_id}.pdf"

        document = {
            "document_id": document_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "status": "uploaded",
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        }

        file_path.write_bytes(pdf_bytes)

        try:
            create_document(document)

        except Exception as exc:
            file_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=500,
                detail="Unable to save document metadata.",
            ) from exc

        return {
            "message": "Document uploaded successfully.",
            "document": document,
        }

    finally:
        await file.close()


@router.get(
    "/documents",
    response_model=DocumentListResponse,
)
def get_documents():

    documents = get_all_documents()

    return {
        "total": len(documents),
        "documents": documents,
    }


@router.get(
    "/documents/{document_id}",
    response_model=DocumentResponse,
)
def get_document_details(document_id: str):

    document = get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return document




@router.post(
    "/documents/{document_id}/process",
    response_model=ProcessDocumentResponse,
)
def process_document(document_id: str):
    document = get_document(document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    if document["status"] == "completed":
        raise HTTPException(status_code=409, detail="Document has already been processed.")

    if document["status"] == "processing":
        raise HTTPException(status_code=409, detail="Document is already being processed.")

    file_path = UPLOAD_DIR / f"{document_id}.pdf"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Uploaded PDF file not found.")

    update_document_status(document_id, "processing")

    try:
        pdf_bytes = file_path.read_bytes()

        result = ingest_document(
            pdf_bytes=pdf_bytes,
            document_id=document_id,
        )

        update_document_status(document_id, "completed")

        return {
            "message": "Document processed successfully.",
            "document_id": document_id,
            "status": result["status"],
        }

    except ValueError as exc:
        logger.warning(
            "Document processing rejected for document_id=%s: %s",
            document_id,
            exc,
        )
        update_document_status(document_id, "failed")

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception:
        logger.exception(
            "Unexpected document processing failure: document_id=%s",
            document_id,
        )
        update_document_status(document_id, "failed")

        raise HTTPException(
            status_code=500,
            detail="Document processing failed. Check server logs.",
        )




@router.delete(
    "/documents/{document_id}",
    response_model=DeleteDocumentResponse,
)
def delete_document_endpoint(document_id: str):

    document = get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    if document["status"] == "processing":
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a document while it is processing.",
        )

    file_path = UPLOAD_DIR / f"{document_id}.pdf"

    try:
        # 1. Remove vectors belonging to this document
        delete_document_chunks(document_id)

        # 2. Remove the uploaded PDF
        file_path.unlink(missing_ok=True)

        # 3. Remove SQLite metadata
        delete_document(document_id)

        return {
            "message": "Document and associated data deleted successfully.",
            "document_id": document_id,
            "status": "deleted",
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Document deletion failed. Check storage consistency.",
        ) from exc
