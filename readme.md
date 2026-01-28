
# DocQuery AI — LLM-Powered Document Intelligence System

DocQuery AI is a full-stack Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask natural language questions, with answers generated strictly from document content.



## Running the Project Locally

### Prerequisites

- Node.js
- Python 3.10+
- Docker

### Steps

1. Start Redis
   docker start redis
2. Start Python worker
   cd ai-service
   python worker.py
3. Start Python AI service
   python app.py
4. Start Node backend
   cd backend
   node index.js
5. Start frontend
   cd frontend
   npm start

## Problem Statement

Organizations deal with large volumes of unstructured documents such as PDFs, DOCX files, and text files. Extracting accurate answers from these documents manually is slow, error-prone, and inefficient.

Traditional LLM-based chat systems also suffer from hallucinations when asked questions without proper grounding in source documents.


## Solution Overview

DocQuery AI solves this problem using Retrieval-Augmented Generation (RAG):

- Documents are ingested, chunked, and embedded into a vector database (FAISS)
- At query time, relevant chunks are retrieved using semantic search
- A large language model (Gemini) generates answers strictly from the retrieved context
- Asynchronous ingestion ensures scalability and responsiveness

## System Architecture

The system is built as a multi-service architecture:

Frontend (React)
   ↓
Node.js API Gateway
   ├── File upload
   ├── Redis job enqueue
   ├── Query proxy
   ↓
Redis (Job Queue)
   ↓
Python Worker
   ├── Document parsing
   ├── Chunking
   ├── Embedding
   ├── FAISS indexing
   ↓
Python AI Service (Flask)
   ├── Vector retrieval
   ├── Prompt construction
   └── LLM answer generation


## Tech Stack

### Frontend

- React — Simple and component-based UI
- Material UI — Dark theme, accessibility, rapid UI development

### Backend

- Node.js + Express — API gateway and async I/O
- Redis — Queue-based asynchronous ingestion
- Python — AI and NLP processing

### AI & Data

- LangChain — Document loading, chunking, orchestration
- FAISS — Fast vector similarity search
- HuggingFace Embeddings (MiniLM) — Lightweight, fast embeddings
- Gemini API — LLM for grounded answer generation

### Infrastructure

- Docker — Running Redis locally


## RAG Pipeline

### Ingestion Phase (Asynchronous)

1. User uploads a document via the frontend
2. Node.js stores the file and pushes a job to Redis
3. Python worker consumes the job and:
   - Parses the document
   - Splits it into overlapping chunks
   - Generates embeddings
   - Stores vectors in FAISS

### Query Phase (Synchronous)

1. User submits a question
2. Node.js forwards the query to the Python AI service
3. Relevant chunks are retrieved from FAISS
4. A grounded prompt is constructed
5. Gemini generates an answer strictly from retrieved context


## Key Design Decisions

- Separation of concerns between Node.js (API) and Python (AI) enables independent scaling
- Redis is used as a job queue to avoid blocking uploads
- FAISS provides fast, local vector search without external dependencies
- LLM is used only at query time to reduce cost and hallucinations
