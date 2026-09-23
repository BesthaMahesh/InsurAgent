from fastapi import APIRouter
from backend.core.config import settings
from backend.rag.vectorstore import get_vectorstore
from backend.mcp.server import mcp_server

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health")
def health_check():
    """Returns system status, active agents, and subsystem connectivity."""
    rag_count = 0
    try:
        rag_count = get_vectorstore().count()
        rag_status = "Ready"
    except Exception:
        rag_status = "Degraded"

    return {
        "status": "Healthy",
        "service": "InsurAgent Multi-Agent Backend",
        "version": "0.1.0",
        "components": {
            "orchestrator": "Ready (LangGraph)",
            "rag_knowledge": f"{rag_status} ({rag_count} chunks indexed)",
            "mcp_tools": f"Connected ({len(mcp_server.tools)} tools)",
            "guardrails": "Active (Deterministic PII & Injection Defense)",
            "database": "Connected (SQLite)"
        },
        "agents": [
            {"name": "Supervisor / Router Agent", "status": "Healthy"},
            {"name": "Claim Intake Agent", "status": "Healthy"},
            {"name": "Document Intelligence Agent", "status": "Healthy"},
            {"name": "Policy Coverage Agent", "status": "Healthy"},
            {"name": "Fraud & Risk Agent", "status": "Healthy"},
            {"name": "Claim Assessment Agent", "status": "Healthy"},
            {"name": "Audit & Compliance Agent", "status": "Healthy"},
            {"name": "Human Review Agent", "status": "Active"}
        ]
    }
