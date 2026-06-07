AI Knowledge Assistant

A production-style Retrieval-Augmented Generation (RAG) platform that allows users to upload documents, add text notes, index YouTube videos, and ask grounded questions against their personal knowledge base.

The system combines semantic search, keyword search, and LLM-powered answer generation to provide accurate, source-backed responses.

Features
Multi-Source Knowledge Ingestion
PDF Documents
Upload PDF files
Automatic text extraction
Chunking and indexing
Semantic retrieval
Text Sources
Add custom notes
Store knowledge snippets
Index instantly
Query alongside documents
YouTube Videos
Extract transcripts
Index video content
Ask questions about videos
Generate summaries and insights
Hybrid Retrieval

Combines:

Semantic Search
Gemini Embeddings
FAISS Vector Database

Finds conceptually similar content even when wording differs.

Keyword Search
BM25 Retrieval

Finds exact matches and important keywords.

Hybrid Ranking

Results from both systems are:

Merged
Deduplicated
Ranked

before being passed to the LLM.

Grounded Answer Generation

Answers are generated only from retrieved context.

Benefits:

Reduced hallucinations
Source-backed responses
Explainable retrieval
Better factual accuracy
Multi-User Isolation

Each user receives an isolated vector store.

```text
data/
└── vector_store/
    ├── user_a/
    │   ├── index.faiss
    │   └── index_meta.json
    │
    └── user_b/
        ├── index.faiss
        └── index_meta.json
```

Benefits:

Secure retrieval
No document leakage
Cloud-ready architecture
Scalable design
Architecture
                 
```text
                    React Frontend
                           │
                           ▼
                    FastAPI Backend
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼

    PDF Upload       Text Sources      YouTube URLs

        │                  │                  │
        └──────────────────┴──────────────────┘
                           │
                           ▼

                Ingestion Pipeline

                           │

                    Source Loader
                           │
                           ▼

                     Chunking
                           │
                           ▼

                  Gemini Embeddings
                           │
                           ▼

                  User FAISS Index

                           │
                           ▼

                  Hybrid Retrieval

               Semantic + BM25 Search

                           │
                           ▼

                    Context Builder
                           │
                           ▼

                  Gemini Generation
                           │
                           ▼

                    Final Response
```
Tech Stack
Frontend
React
Vite
TailwindCSS
Backend
FastAPI
Python
Retrieval
FAISS
BM25
LLM
Google Gemini
Embeddings
Gemini Embeddings
Data Storage
JSON Registry
Local File Storage
Project Structure

```text
AI-Knowledge-Assistant/

├── backend/
│
│   ├── routes/
│   │   ├── chat.py
│   │   └── sources.py
│   │
│   ├── services/
│   │   ├── query_service.py
│   │   ├── registry_service.py
│   │   └── storage_service.py
│   │
│   ├── src/
│   │
│   │   ├── ingestion/
│   │   │
│   │   │   ├── loaders/
│   │   │   │   ├── pdf_loader.py
│   │   │   │   ├── text_loader.py
│   │   │   │   └── youtube_loader.py
│   │   │
│   │   │   ├── chunkers/
│   │   │   ├── embedders/
│   │   │   ├── indexers/
│   │   │   └── pipeline.py
│   │
│   │   ├── retrieval/
│   │   │   ├── retriever.py
│   │   │   └── keyword_retriever.py
│   │
│   │   └── generation/
│   │       └── generator.py
│
│   └── data/
│       ├── docs/
│       ├── notes/
│       ├── registry/
│       └── vector_store/
│
└── frontend/
```
Installation
Backend Setup
cd backend

text```python -m venv .venv```

Windows:

text ``` .venv\Scripts\activate ```

Install dependencies:

pip install -r requirements.txt
Environment Variables

Create:

backend/.env

Add:

GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
Run Backend
uvicorn app:app --reload

Backend URL:

http://127.0.0.1:8000
Frontend Setup
cd frontend

npm install

Run:

npm run dev

Frontend URL:

http://localhost:5173
API Endpoints
Upload PDF
POST /api/sources/upload
Add Text Source
POST /api/sources/text

Example:

{
  "title": "AWS Notes",
  "text": "AWS provides EC2, S3, Lambda, SageMaker and Bedrock."
}
Add YouTube Video
POST /api/sources/youtube

Example:

{
  "title": "AI Video",
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
List Sources
GET /api/sources
Query Knowledge Base
POST /api/chat/query

Example:

{
  "question": "What AWS services are mentioned?",
  "source_ids": [
    "src_123456"
  ],
  "top_k": 5
}
Example Workflow
Upload PDF
Resume.pdf

Ask:

What cloud platforms has the candidate worked with?
Add Text Notes
AWS provides EC2, S3, Lambda and Bedrock.

Ask:

What AWS services are mentioned?
Add YouTube Video
https://www.youtube.com/watch?v=bhzZXQhxWV8

Ask:

What is this video about?
Current Status
PDF Ingestion            ✅
Text Ingestion           ✅
YouTube Ingestion        ✅
Gemini Embeddings        ✅
FAISS Vector Search      ✅
BM25 Retrieval           ✅
Hybrid Search            ✅
Multi-User Isolation     ✅
React UI                 ✅
Source Citations         ✅

Authentication           🔄 Planned
Streaming Responses      🔄 Planned
Chat History             🔄 Planned
Cloud Deployment         🔄 Planned
Reranking Models         🔄 Planned
Future Enhancements
JWT Authentication
PostgreSQL Metadata Store
Streaming Responses
Pinecone / Qdrant Integration
OCR for Scanned PDFs
Chat History
Source Highlighting
Document Summarization
Multi-Agent Retrieval
Evaluation Framework
Cloud Deployment (AWS/Azure/GCP)
Author

Satya Damarla

AI/ML Engineer

Specialties:

Retrieval-Augmented Generation (RAG)
LLM Applications
MLOps
AI Platforms
Vector Search
Production AI Systems
