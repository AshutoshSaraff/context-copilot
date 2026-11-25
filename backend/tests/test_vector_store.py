
from uuid import uuid4

from backend.services.embeddings import generate_embeddings
from backend.services.vector_store import store_chunks, search_chunks


def test_vector_storage_and_retrieval():
    document_id = str(uuid4())

    chunks = [
        {
            "chunk_id": str(uuid4()),
            "page_number": 1,
            "text": "Python is a programming language.",
        },
        {
            "chunk_id": str(uuid4()),
            "page_number": 2,
            "text": "FastAPI is used to build APIs with Python.",
        },
    ]

    texts = [chunk["text"] for chunk in chunks]

    embeddings = generate_embeddings(texts)

    store_chunks(chunks, embeddings, document_id)

    query_embedding = generate_embeddings(
        ["Which framework is used to build Python APIs?"]
    )[0]

    results = search_chunks(
        query_embedding,
        document_id,
        top_k=2,
    )

    assert len(results["documents"][0]) > 0
    assert len(results["metadatas"][0]) > 0
    assert len(results["distances"][0]) > 0
