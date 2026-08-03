# aws-serverless-observability

This repository contains a serverless observability stack with a FastAPI backend, PostgreSQL-backed telemetry data, an ETL pipeline, and a React/Vite frontend.

## What has been implemented

### RAG flow
- Telemetry data is pulled from PostgreSQL and converted into readable text chunks.
- Relevant chunks are retrieved using a lightweight vector search layer.
- The generator now tries a local LLM via Ollama for grounded answers.
- If Ollama is unavailable, the app still returns a safe fallback response.

### Backend API
- POST /rag/query for answering natural-language questions over telemetry data.
- POST /rag/reindex to rebuild the in-memory index from the latest database content.

### Local AI support
- Added environment settings for Ollama:
  - OLLAMA_BASE_URL
  - OLLAMA_MODEL
- Default model is llama3.2:3b.

### Tests
- Added generator-focused tests covering the LLM path and fallback behavior.

## Run locally

### Backend
```bash
cd backend
. .venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Ollama setup
If you want real LLM-generated answers, install Ollama and pull a model:

```bash
ollama pull llama3.2:3b
ollama serve
```

If Ollama is not running, the RAG endpoint will still work and use the fallback response.

## Important note
The current RAG implementation is lightweight and demo-friendly, but it already supports a real LLM path for better answer generation and clearer observability insights.
