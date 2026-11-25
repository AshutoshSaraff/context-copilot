
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str | None
    status: str
    uploaded_at: str


class DocumentUploadResponse(BaseModel):
    message: str
    document: DocumentResponse


class DocumentListResponse(BaseModel):
    total: int
    documents: list[DocumentResponse]


class ProcessDocumentResponse(BaseModel):
    message: str
    document_id: str
    status: str


class DeleteDocumentResponse(BaseModel):
    message: str
    document_id: str
    status: str
