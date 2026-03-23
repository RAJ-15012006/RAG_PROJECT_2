from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ..models.chat import ChatRequest
from ..rag_pipeline import format_sources
import json
import asyncio
import re

router = APIRouter()
rag_data = None

def clean_response(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

async def stream_response(question: str):
    try:
        if rag_data is None:
            raise RuntimeError("RAG not initialized")

        chain = rag_data["chain"]
        retriever = rag_data["retriever"]

        docs = await asyncio.to_thread(retriever.invoke, question)
        sources = format_sources(docs)

        full = ""
        async for chunk in chain.astream(question):
            full += chunk

        answer = clean_response(full)

        yield f"data: {json.dumps({'type': 'answer', 'content': answer})}\n\n"
        yield f"data: {json.dumps({'type': 'sources', 'content': sources})}\n\n"
        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

@router.post("/chat")
async def chat(request: ChatRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    return StreamingResponse(stream_response(request.question), media_type="text/event-stream")
