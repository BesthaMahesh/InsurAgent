import os
import re
import math
import hashlib
from pathlib import Path
from typing import List, Optional, Dict, Any
import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from backend.core.config import settings, BASE_DIR
from backend.core.logging_config import logger

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
    "to", "was", "were", "will", "with", "what", "how", "under", "which", "does"
}


class LightweightSemanticEmbedding(EmbeddingFunction[Documents]):
    """
    High-speed, memory-efficient semantic embedding function (512 dimensions).
    Uses non-negative subword feature hashing and term frequency weighting with L2 normalization.
    Consumes <1MB memory, eliminating ONNX / PyTorch OOM crashes on cloud containers.
    """
    def __init__(self, dim: int = 512):
        self.dim = dim

    @staticmethod
    def name() -> str:
        return "lightweight_semantic_v3"


    def get_config(self) -> Dict[str, Any]:
        return {"dim": self.dim}

    @classmethod
    def build_from_config(cls, config: Dict[str, Any]) -> "LightweightSemanticEmbedding":
        return cls(dim=config.get("dim", 512))


    def _embed_text(self, text: str) -> List[float]:
        vec = [0.0] * self.dim
        if not text:
            return vec
        
        words = re.findall(r"\b[a-zA-Z0-9_\-]+\b", text.lower())
        filtered = [w for w in words if w not in STOPWORDS and len(w) > 1]
        
        # Word features + adjacent bigrams for phrase matching
        features = list(filtered)
        for i in range(len(filtered) - 1):
            features.append(f"{filtered[i]}_{filtered[i+1]}")
            
        for f in features:
            h = int(hashlib.sha256(f.encode("utf-8")).hexdigest()[:8], 16)
            idx = h % self.dim
            vec[idx] += 1.0

        # L2 normalize
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    def __call__(self, input: Documents) -> Embeddings:
        return [self._embed_text(doc) for doc in input]


_chroma_client = None
_collection = None
_is_ingesting = False
_embedding_fn = LightweightSemanticEmbedding(dim=512)
COLLECTION_NAME = "insuragent_knowledge_base_v3"




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
    global _collection, _is_ingesting, _embedding_fn
    client = get_chroma_client()
    try:
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=_embedding_fn,
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
        try:
            _collection = client.get_collection(COLLECTION_NAME, embedding_function=_embedding_fn)
        except Exception:
            _collection = client.get_or_create_collection(
                name=COLLECTION_NAME,
                embedding_function=_embedding_fn,
                metadata={"hnsw:space": "cosine"}
            )
    return _collection


