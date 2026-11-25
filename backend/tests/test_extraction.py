
import pymupdf
import pytest

from backend.services.extraction import extract_pages


def create_test_pdf():
    document = pymupdf.open()

    page = document.new_page()
    page.insert_text(
        (72, 72),
        "Context Copilot PDF extraction test"
    )

    pdf_bytes = document.tobytes()
    document.close()

    return pdf_bytes


def test_extract_pages():
    pdf_bytes = create_test_pdf()

    pages = extract_pages(pdf_bytes)

    assert len(pages) == 1
    assert pages[0]["page_number"] == 1
    assert "Context Copilot" in pages[0]["text"]


def test_empty_pdf():
    with pytest.raises(ValueError):
        extract_pages(b"")


def test_invalid_pdf():
    with pytest.raises(ValueError):
        extract_pages(b"this is not a PDF")
