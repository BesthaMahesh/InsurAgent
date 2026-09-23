from typing import List, Dict, Any, Optional
from backend.core.config import settings
from backend.core.logging_config import logger
from backend.rag.vectorstore import get_vectorstore
from backend.models.response import PolicyClauseEvidence


class PolicyRetriever:
    """Retrieves relevant policy clauses and guidelines from the vector store."""

    def __init__(self, top_k: Optional[int] = None):
        self.top_k = top_k or settings.RAG_TOP_K

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[PolicyClauseEvidence]:
        """Queries vector database and returns grounded policy clauses."""
        k = top_k or self.top_k
        if not query or not query.strip():
            return []

        try:
            collection = get_vectorstore()
            count = collection.count()
            if count == 0:
                logger.warning("RAG collection is currently empty.")
                return []

            results = collection.query(
                query_texts=[query],
                n_results=min(k, count),
                include=["documents", "metadatas", "distances"]
            )

            clauses: List[PolicyClauseEvidence] = []
            if results and results.get("documents") and results["documents"][0]:
                docs = results["documents"][0]
                metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
                distances = results["distances"][0] if results.get("distances") else [0.0] * len(docs)

                for doc_text, meta, dist in zip(docs, metas, distances):
                    # Convert cosine distance to similarity score
                    sim_score = max(0.0, 1.0 - (dist if dist is not None else 0.5))
                    
                    # Filtering noise if score is extremely low
                    if sim_score < 0.20:
                        continue

                    clauses.append(
                        PolicyClauseEvidence(
                            source_doc=meta.get("source", "Knowledge Base"),
                            section=meta.get("section", "General Clause"),
                            clause_text=doc_text,
                            relevance_score=round(sim_score, 3)
                        )
                    )

            logger.info(f"Retrieved {len(clauses)} policy clauses for query: '{query[:50]}...'")
            return clauses

        except Exception as e:
            logger.error(f"Error during RAG retrieval: {e}")
            return []

    def format_context_for_prompt(self, clauses: List[PolicyClauseEvidence]) -> str:
        """Formats retrieved clauses into an evidence block for LLM prompts."""
        if not clauses:
            return "NO RELEVANT POLICY EVIDENCE FOUND IN KNOWLEDGE BASE."
        
        blocks = []
        for i, c in enumerate(clauses, start=1):
            score_str = f" (Relevance: {c.relevance_score})" if c.relevance_score else ""
            blocks.append(
                f"--- EVIDENCE [{i}] ---\n"
                f"Source Document: {c.source_doc}\n"
                f"Section: {c.section}{score_str}\n"
                f"Clause Content:\n{c.clause_text}"
            )
        return "\n\n".join(blocks)
