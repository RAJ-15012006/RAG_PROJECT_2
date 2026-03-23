from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Transformer Research Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Transformer Research Assistant API is running"}

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    try:
        from .rag_pipeline import initialize_rag
        from .routes import chat as chat_module

        logger.info("Initializing RAG pipeline...")
        rag_data = initialize_rag()
        chat_module.rag_data = rag_data
        app.include_router(chat_module.router, prefix="/api", tags=["Chat"])
        logger.info("✅ RAG pipeline ready. Server is live on http://localhost:8002")
    except Exception as e:
        logger.error(f"FATAL: {e}", exc_info=True)
        sys.exit(1)
