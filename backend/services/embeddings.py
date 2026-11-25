
from functools import lru_cache

from google import genai
from google.genai import types

from backend.app.core.config import settings


@lru_cache(maxsize=1)
def get_embedding_client():
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    return genai.Client(api_key=settings.gemini_api_key)


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate document embeddings for multiple text chunks."""

    if not texts:
        return []

    if any(not isinstance(text, str) or not text.strip() for text in texts):
        raise ValueError("All input texts must be non-empty strings.")

    client = get_embedding_client()

    response = client.models.embed_content(
        model=settings.embedding_model,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT"
        ),
    )

    if not response.embeddings:
        raise RuntimeError("Gemini returned no embeddings.")

    if len(response.embeddings) != len(texts):
        raise RuntimeError("Embedding count does not match input count.")

    return [
        embedding.values
        for embedding in response.embeddings
    ]


def generate_query_embedding(text: str) -> list[float]:
    """Generate an embedding for a user's search query."""

    if not text or not text.strip():
        raise ValueError("Query cannot be empty.")

    client = get_embedding_client()

    response = client.models.embed_content(
        model=settings.embedding_model,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY"
        ),
    )

    if not response.embeddings:
        raise RuntimeError("Gemini returned no query embedding.")

    return response.embeddings[0].values
