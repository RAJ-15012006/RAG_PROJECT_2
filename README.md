# Transformer Research Assistant

A production-quality RAG (Retrieval-Augmented Generation) chatbot designed to answer questions about the seminal research paper: **"Attention Is All You Need"**.

## Features

- **Backend**: FastAPI (Python) with LangChain, ChromaDB, and Ollama.
- **Frontend**: Next.js (TypeScript) with TailwindCSS, shadcn/ui, and Three.js.
- **RAG Pipeline**: PDF chunking, embeddings (nomic-embed-text), and retrieval (llama3).
- **Streaming Responses**: Real-time answer generation with SSE (Server-Sent Events).
- **Source Citations**: Automatic source attribution with page numbers from the PDF.
- **3D Visualization**: Interactive neural network attention flow background using React Three Fiber.
- **Glassmorphism UI**: Modern, futuristic dashboard design.

## Project Structure

```text
project/
├── backend/            # FastAPI Backend
│   ├── data/           # PDF and Vector Store
│   ├── models/         # Pydantic models
│   ├── routes/         # API endpoints
│   ├── main.py         # Entry point
│   └── rag_pipeline.py  # RAG Logic
└── frontend/           # Next.js Frontend
    ├── app/            # Next.js App Router
    ├── components/     # UI & 3D Components
    └── lib/            # Utilities
```

## Setup Instructions

### 1. Prerequisites
- **Ollama** installed and running.
- Pull required models:
  ```bash
  ollama pull llama3
  ollama pull nomic-embed-text
  ```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Example Queries
- "What is the core idea of the Transformer architecture?"
- "Explain the Scaled Dot-Product Attention mechanism."
- "What are the advantages of self-attention over recurrent layers?"
- "How are positional encodings calculated?"
- "What was the training configuration for the base model?"

## Technical Details

- **Embeddings**: `nomic-embed-text` via Ollama.
- **LLM**: `llama3` via Ollama.
- **Vector DB**: ChromaDB for efficient similarity search.
- **Frontend Tech**: Next.js 14, Three.js, Tailwind CSS, Framer Motion.
