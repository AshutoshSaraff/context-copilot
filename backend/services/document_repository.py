
import sqlite3
from pathlib import Path

# Database location: backend/storage/context_copilot.db
BACKEND_DIR = Path(__file__).resolve().parents[1]
STORAGE_DIR = BACKEND_DIR / "storage"
DATABASE_PATH = STORAGE_DIR / "context_copilot.db"

STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                content_type TEXT,
                status TEXT NOT NULL,
                uploaded_at TEXT NOT NULL
            )
        """)

        connection.commit()

    finally:
        connection.close()


def create_document(document: dict) -> None:
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO documents (
                document_id,
                filename,
                content_type,
                status,
                uploaded_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                document["document_id"],
                document["filename"],
                document["content_type"],
                document["status"],
                document["uploaded_at"],
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_document(document_id: str) -> dict | None:
    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT * FROM documents WHERE document_id = ?",
            (document_id,),
        ).fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def get_all_documents() -> list[dict]:
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT * FROM documents
            ORDER BY uploaded_at DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def update_document_status(document_id: str, status: str) -> None:
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE documents
            SET status = ?
            WHERE document_id = ?
            """,
            (status, document_id),
        )

        connection.commit()

        if cursor.rowcount == 0:
            raise ValueError("Document not found.")

    finally:
        connection.close()


# Create the database and table when this module is imported.
initialize_database()


def delete_document(document_id: str) -> None:
    """Delete document metadata from SQLite."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM documents WHERE document_id = ?",
            (document_id,),
        )

        connection.commit()

        if cursor.rowcount == 0:
            raise ValueError("Document not found.")

    finally:
        connection.close()
