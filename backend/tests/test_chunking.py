
import pytest

from backend.services.chunking import chunk_pages


def test_chunk_creation():
    pages = [
        {"page_number": 1, "text": "A" * 2500}
    ]

    chunks = chunk_pages(pages, 1000, 200)

    assert len(chunks) == 3
    assert len(chunks[0]["text"]) == 1000
    assert chunks[0]["page_number"] == 1


def test_chunk_overlap():
    pages = [{"page_number": 1, "text": "A" * 1500}]

    chunks = chunk_pages(pages, 1000, 200)

    assert chunks[0]["text"][-200:] == chunks[1]["text"][:200]


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        chunk_pages([], 0, 0)


def test_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_pages([], 1000, 1000)
