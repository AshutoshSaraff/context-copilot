
# Context Copilot

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their contents.

## Features

- PDF document upload and text extraction
- Text chunking with overlapping windows
- Gemini-powered document embeddings
- Persistent vector storage using ChromaDB
- Semantic search and document-specific retrieval
- Context-grounded answers using Gemini
- Source references with page numbers
- Document management and deletion
- FastAPI backend and Streamlit frontend

## Architecture

PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Gemini Embeddings
    ↓
ChromaDB
    ↓
User Question
    ↓
Query Embedding
    ↓
Semantic Retrieval
    ↓
Relevant Context
    ↓
Gemini Answer Generation
    ↓
Answer with Sources

## Tech Stack

- Python 3.11
- FastAPI
- Streamlit
- Google Gemini API
- ChromaDB
- PyMuPDF
- SQLite
- Docker

## Project Structure

context-copilot/
├── backend/
│   ├── app/
│   ├── services/
│   ├── tests/
│   ├── storage/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
├── sample_documents/
├── .env.example
├── .gitignore
├── .dockerignore
└── README.md

## Environment Variables

Create a `.env` file in the project root.

Required variables:

- GEMINI_API_KEY
- GEMINI_MODEL
- EMBEDDING_MODEL

Never commit your actual `.env` file.

## Local Setup

### 1. Clone the repository

git clone YOUR_REPOSITORY_URL
cd context-copilot

### 2. Create a virtual environment

python -m venv .venv

### 3. Activate it

Windows:

.venv\Scripts\activate

### 4. Install backend dependencies

pip install -r backend/requirements.txt

### 5. Install frontend dependencies

pip install -r frontend/requirements.txt

### 6. Configure environment variables

Create `.env` using `.env.example` as a reference.

### 7. Start the backend

python -m uvicorn backend.app.main:app --reload

Backend API:
http://127.0.0.1:8000

API documentation:
http://127.0.0.1:8000/docs

### 8. Start the frontend

streamlit run frontend/streamlit_app.py

## Running Tests

python -m pytest -v

## Deployment

The backend is containerized using Docker.
The frontend can be deployed as a separate Streamlit application.

Persistent storage is required for SQLite, uploaded documents and ChromaDB.

## Current Limitations

- No user authentication yet
- No multi-user access control
- Retrieval quality depends on document quality and chunking
- Persistent storage is required in production
