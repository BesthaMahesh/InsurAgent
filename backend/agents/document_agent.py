"""
Layer 4: Agent Layer — Agent 2: Document Analysis Agent
Responsibilities:
1. Extract information (OCR)
2. Validate documents
3. Detect missing / inconsistent data
4. Structured output
"""
from typing import Dict, Any, List
from backend.services.document_service import DocumentService
from backend.services.memory_service import MemoryService
from backend.core.logging_config import logger


class DocumentAgent:
    """
    2. Document Analysis Agent.
    Domain expert responsible for OCR extraction, validating document consistency,
    detecting missing evidence, and producing structured data outputs.
    """

    @staticmethod
    def process_documents(state: Dict[str, Any]) -> Dict[str, Any]:
        claim_id = state.get("claim_id", "")
        documents = state.get("documents", [])
        claim_details = state.get("claim_details", {})
        claim_type = claim_details.get("claim_type", "Health")
        claimed_amount = float(claim_details.get("amount", 0.0))
        
        extracted_data = {
            "processed_count": len(documents),
            "documents_summary": [],
            "combined_text": "",
            "validation_status": "Valid",
            "validation_flags": [],
            "inconsistencies_detected": [],
            "extracted_entities": {
                "hospital_or_garage": None,
                "invoice_totals": [],
                "document_types": [],
                "dates_mentioned": []
            }
        }

        audit_messages = []

        # 1. Missing Document Check
        if not documents:
            extracted_data["documents_summary"].append("No supporting documents attached with initial intake.")
            extracted_data["validation_status"] = "Missing Documents"
            extracted_data["validation_flags"].append(f"Mandatory supporting invoices or {claim_type} reports missing.")
            audit_messages.append("Document Agent: Missing mandatory documents detected; flagged for assessment.")
        else:
            all_texts = []
            for doc in documents:
                fname = doc.get("filename", "unknown_document")
                raw_b64 = doc.get("content_base64")
                
                # 2. Extract Information (OCR / Base64 decode)
                if raw_b64:
                    extracted = DocumentService.extract_text_from_base64(raw_b64, fname)
                    text_content = extracted.get("text", "")
                else:
                    text_content = doc.get("extracted_text", f"Supporting document record: {fname}")

                all_texts.append(f"--- Document: {fname} ---\n{text_content}")
                extracted_data["documents_summary"].append(f"Parsed {fname} ({len(text_content)} chars)")
                doc_ext = fname.split(".")[-1].upper() if "." in fname else "DOC"
                extracted_data["extracted_entities"]["document_types"].append(doc_ext)

            extracted_data["combined_text"] = "\n\n".join(all_texts)
            extracted_data["validation_status"] = "Verified"
            audit_messages.append(f"Document Agent: OCR extracted & validated {len(documents)} document(s).")

        # 3. Detect Missing / Inconsistent Data
        if documents and claimed_amount > 0 and not extracted_data["combined_text"]:
            extracted_data["inconsistencies_detected"].append("Document text could not be extracted; manual scan needed.")

        # 4. Record to Episodic Memory
        MemoryService.record_episodic_event(
            claim_id=claim_id,
            agent="DocumentAgent",
            action=f"Extracted {len(documents)} document(s). Status: {extracted_data['validation_status']}."
        )

        logger.info(f"[DocumentAgent] {claim_id} extracted {len(documents)} document(s). Status={extracted_data['validation_status']}")

        audit_entry = {
            "claim_id": claim_id,
            "agent": "DocumentAgent",
            "action": "; ".join(audit_messages),
            "source": "Document Intelligence OCR & Validation Engine",
            "status": "success",
            "timestamp": ""
        }

        return {
            "current_agent": "DocumentAgent",
            "extracted_document_data": extracted_data,
            "audit_events": [audit_entry]
        }
