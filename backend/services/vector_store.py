
import chromadb

from backend.app.core.config import settings


# Initialize persistent ChromaDB client
client = chromadb.PersistentClient(
    path=str(settings.chroma_persist_dir)
)


# Create or retrieve our collection
collection = client.get_or_create_collection(
    name="context_copilot",
    metadata={"hnsw:space": "cosine"},
)


def store_chunks(
    chunks: list[dict],
    embeddings: list[list[float]],
    document_id: str,
) -> None:
    """Store document chunks and their embeddings."""

    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings count mismatch.")

    if not chunks:
        return

    collection.upsert(
        ids=[chunk["chunk_id"] for chunk in chunks],
        embeddings=embeddings,
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[
            {
                "document_id": document_id,
                "page_number": chunk["page_number"],
            }
            for chunk in chunks
        ],
    )


def search_chunks(
    query_embedding: list[float],
    document_id: str,
    top_k: int | None = None,
) -> dict:
    """Retrieve the most similar chunks for a document."""

    if not query_embedding:
        raise ValueError("Query embedding cannot be empty.")

    if not document_id:
        raise ValueError("Document ID cannot be empty.")

    if top_k is None:
        top_k = settings.retrieval_top_k

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"document_id": document_id},
        include=["documents", "metadatas", "distances"],
    )

    return results


def delete_document_chunks(document_id: str) -> None:
    """Delete all ChromaDB chunks belonging to one document."""

    if not document_id:
        raise ValueError("Document ID cannot be empty.")

    collection.delete(
        where={"document_id": document_id}
    )
