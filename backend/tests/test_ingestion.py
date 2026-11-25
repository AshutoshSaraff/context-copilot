
import pymupdf

from uuid import uuid4

from backend.services.ingestion import ingest_document


def test_complete_document_ingestion():
    # Create a sample PDF in memory
    pdf = pymupdf.open()

    page = pdf.new_page()
    page.insert_text(
        (72, 72),
        "Python is a programming language. "
        "FastAPI is a framework used to build APIs."
    )

    pdf_bytes = pdf.tobytes()
    pdf.close()

    # Run the complete ingestion pipeline
    document_id = str(uuid4())

    result = ingest_document(
        pdf_bytes=pdf_bytes,
        document_id=document_id,
    )

    assert result["status"] == "completed"
    assert result["pages_processed"] == 1
    assert result["chunks_created"] > 0
    assert result["embeddings_generated"] == result["chunks_created"]
