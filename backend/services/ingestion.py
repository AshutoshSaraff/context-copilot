
from backend.services.extraction import extract_pages
from backend.services.chunking import chunk_pages
from backend.services.embeddings import generate_embeddings
from backend.services.vector_store import store_chunks


def ingest_document(
    pdf_bytes: bytes,
    document_id: str,
) -> dict:
    """Process a PDF and store its chunks in ChromaDB."""

    if not document_id:
        raise ValueError("Document ID cannot be empty.")

    # Step 1: Extract text from PDF pages
    pages = extract_pages(pdf_bytes)

    # Step 2: Split extracted text into chunks
    chunks = chunk_pages(pages)

    if not chunks:
        raise ValueError("No text chunks were generated.")

    # Step 3: Generate embeddings for every chunk
    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)

    # Step 4: Store chunks and embeddings in ChromaDB
    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        document_id=document_id,
    )

    return {
        "document_id": document_id,
        "pages_processed": len(pages),
        "chunks_created": len(chunks),
        "embeddings_generated": len(embeddings),
        "status": "completed",
    }
