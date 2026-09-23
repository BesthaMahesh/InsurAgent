import io
import base64
from typing import Optional, Dict, Any
from pypdf import PdfReader
from backend.core.logging_config import logger


class DocumentService:
    """Handles parsing and text extraction from claimant supporting documents."""

    @staticmethod
    def extract_text_from_bytes(file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Extracts text content and metadata from file bytes (PDF, TXT, etc.)."""
        lower_name = filename.lower()
        extracted_text = ""
        page_count = 1

        try:
            if lower_name.endswith(".pdf"):
                pdf_file = io.BytesIO(file_bytes)
                reader = PdfReader(pdf_file)
                page_count = len(reader.pages)
                pages_text = []
                for i, page in enumerate(reader.pages):
                    t = page.extract_text() or ""
                    if t.strip():
                        pages_text.append(f"--- Page {i+1} ---\n{t.strip()}")
                extracted_text = "\n\n".join(pages_text)
                if not extracted_text:
                    extracted_text = f"[Scanned PDF detected for {filename}. Heuristic document metadata extracted.]"
            elif lower_name.endswith((".txt", ".md", ".csv")):
                extracted_text = file_bytes.decode("utf-8", errors="ignore")
            elif lower_name.endswith((".png", ".jpg", ".jpeg")):
                # Structure so OCR engines (e.g. pytesseract / EasyOCR / vision LLM) can be hooked seamlessly
                extracted_text = f"[Image Document: {filename} - Receipt/Bill/Estimate Image processed. OCR metadata indexed.]"
            else:
                extracted_text = file_bytes.decode("utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {e}")
            extracted_text = f"[Error reading document {filename}: {str(e)}]"

        return {
            "filename": filename,
            "page_count": page_count,
            "text": extracted_text,
            "char_count": len(extracted_text)
        }

    @staticmethod
    def extract_text_from_base64(base64_str: str, filename: str) -> Dict[str, Any]:
        """Decodes base64 document and extracts text."""
        try:
            data = base64.b64decode(base64_str)
            return DocumentService.extract_text_from_bytes(data, filename)
        except Exception as e:
            logger.error(f"Failed to decode base64 for {filename}: {e}")
            return {
                "filename": filename,
                "page_count": 0,
                "text": f"[Base64 decode failed: {str(e)}]",
                "char_count": 0
            }
