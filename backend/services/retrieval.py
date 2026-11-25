
from backend.app.core.config import settings
from backend.services.embeddings import generate_query_embedding
from backend.services.vector_store import search_chunks


def retrieve_relevant_chunks(
    query: str,
    document_id: str,
    top_k: int | None = None,
) -> list[dict]:
    """Find the most relevant chunks for a user's question."""

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not document_id:
        raise ValueError("Document ID cannot be empty.")

    if top_k is None:
        top_k = settings.retrieval_top_k

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    # Step 1: Convert the user's question into an embedding
    query_embedding = generate_query_embedding(query)

    # Step 2: Search ChromaDB using that embedding
    results = search_chunks(
        query_embedding=query_embedding,
        document_id=document_id,
        top_k=top_k,
    )

    # Step 3: Format the retrieved results
    retrieved_chunks = []

    if not results["ids"] or not results["ids"][0]:
        return retrieved_chunks

    for index, chunk_id in enumerate(results["ids"][0]):
        retrieved_chunks.append({
            "chunk_id": chunk_id,
            "text": results["documents"][0][index],
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index],
        })

    return retrieved_chunks
