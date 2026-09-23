import os
from pathlib import Path
from typing import List, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from backend.core.config import settings, BASE_DIR
from backend.core.logging_config import logger

_chroma_client = None
_collection = None
_is_ingesting = False
COLLECTION_NAME = "insuragent_knowledge_base"


def get_chroma_client():
    """Initializes or returns a persistent ChromaDB client."""
    global _chroma_client
    if _chroma_client is None:
        db_path = str(Path(settings.CHROMA_DB_PATH).resolve())
        Path(db_path).mkdir(parents=True, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=db_path)
    return _chroma_client


def get_vectorstore():
    """Returns the Chroma collection for policy knowledge retrieval, auto-ingesting if empty."""
    global _collection, _is_ingesting
    client = get_chroma_client()
    try:
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        if _collection.count() == 0 and not _is_ingesting:
            _is_ingesting = True
            logger.info("Chroma collection empty on startup. Automatically ingesting policy documents...")
            try:
                from backend.rag.ingest import ingest_all_documents
                ingest_all_documents()
            except Exception as ie:
                logger.warning(f"Auto-ingestion warning: {ie}")
            finally:
                _is_ingesting = False
    except Exception as e:
        logger.error(f"Error getting chroma collection: {e}")
        _collection = client.get_collection(COLLECTION_NAME)
    return _collection

