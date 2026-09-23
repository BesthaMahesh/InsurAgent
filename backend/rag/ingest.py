import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any
from backend.core.config import settings, BASE_DIR
from backend.core.logging_config import logger
from backend.rag.vectorstore import get_vectorstore


def chunk_markdown_text(text: str, filename: str, doc_type: str) -> List[Dict[str, Any]]:
    """Splits markdown document into semantic chunks by headers and paragraphs."""
    chunks = []
    sections = text.split("## ")
    
    doc_header = sections[0].strip() if sections else ""
    first_title = doc_header.split("\n")[0].replace("#", "").strip() or filename

    # If document has no ## headings
    if len(sections) == 1:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for i, para in enumerate(paragraphs):
            chunk_id = hashlib.md5(f"{filename}_{i}_{para[:30]}".encode()).hexdigest()
            chunks.append({
                "id": chunk_id,
                "text": para,
                "metadata": {
                    "source": filename,
                    "doc_type": doc_type,
                    "section": f"Paragraph {i+1}",
                    "title": first_title
                }
            })
        return chunks

    # Process sectioned markdown
    for s_idx, section in enumerate(sections[1:], start=1):
        lines = section.split("\n")
        section_title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        
        # Split body if long
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
        if not paragraphs:
            paragraphs = [body]
            
        for p_idx, para in enumerate(paragraphs):
            combined_text = f"## {section_title}\n{para}"
            chunk_id = hashlib.md5(f"{filename}_{section_title}_{p_idx}".encode()).hexdigest()
            chunks.append({
                "id": chunk_id,
                "text": combined_text,
                "metadata": {
                    "source": filename,
                    "doc_type": doc_type,
                    "section": section_title,
                    "title": first_title
                }
            })

    return chunks


def ingest_all_documents() -> int:
    """Scans data directories and ingests all knowledge documents into ChromaDB."""
    collection = get_vectorstore()
    
    data_dirs = {
        "policy": BASE_DIR / "data" / "policies",
        "guideline": BASE_DIR / "data" / "guidelines",
        "compliance": BASE_DIR / "data" / "compliance",
        "faq": BASE_DIR / "data" / "faq"
    }

    all_chunks: List[Dict[str, Any]] = []

    for doc_type, folder in data_dirs.items():
        if not folder.exists():
            continue
        for file_path in folder.glob("*.*"):
            if file_path.suffix.lower() in [".md", ".txt"]:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    chunks = chunk_markdown_text(content, file_path.name, doc_type)
                    all_chunks.extend(chunks)
                    logger.info(f"Loaded {len(chunks)} chunks from {file_path.name}")
                except Exception as e:
                    logger.error(f"Failed to read document {file_path}: {e}")

    if all_chunks:
        ids = [c["id"] for c in all_chunks]
        documents = [c["text"] for c in all_chunks]
        metadatas = [c["metadata"] for c in all_chunks]

        # Upsert into Chroma
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        logger.info(f"Ingested a total of {len(all_chunks)} knowledge base chunks into Chroma.")
    else:
        logger.warning("No knowledge chunks found during ingestion.")

    return len(all_chunks)


if __name__ == "__main__":
    count = ingest_all_documents()
    print(f"Successfully ingested {count} knowledge chunks into InsurAgent RAG store.")
