"""
Client helper for Streamlit and external multi-channel interfaces to interact with all 9 architectural layers.
"""
import base64
import os
from typing import Dict, Any, List, Optional
import httpx
from backend.core.config import settings
from backend.core.logging_config import logger
from backend.services.governance_service import GovernanceService
from backend.services.cost_service import CostService
from backend.services.observability_service import ObservabilityService
from backend.services.memory_service import MemoryService
from backend.mcp.client import MCPClient


class InsurAgentClient:
    """Client helper for Streamlit and external integrations to query backend API and services."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or settings.BACKEND_API_URL).rstrip("/")
        self.mcp = MCPClient()

    def get_health(self) -> Dict[str, Any]:
        try:
            with httpx.Client(timeout=5.0) as client:
                res = client.get(f"{self.base_url}/api/health")
                if res.status_code == 200:
                    return res.json()
        except Exception as e:
            logger.warning(f"Backend API health check fallback to embedded: {e}")
        return {"status": "Standby", "components": {"mode": "Embedded In-Process"}}

    def post_chat(self, query: str, claim_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            with httpx.Client(timeout=45.0) as client:
                payload = {"query": query, "claim_id": claim_id}
                res = client.post(f"{self.base_url}/api/chat", json=payload)
                if res.status_code == 200:
                    return res.json()
                return {"error": res.text, "status_code": res.status_code}
        except Exception as e:
            logger.info(f"Direct in-process chat execution fallback: {e}")
            from backend.graph.workflow import process_claim_graph
            import uuid
            c_id = claim_id or f"CLM-DEMO-{uuid.uuid4().hex[:4].upper()}"
            init_state = {
                "claim_id": c_id,
                "trace_id": f"TRC-{uuid.uuid4().hex[:8].upper()}",
                "persona": "Claimant",
                "channel": "Streamlit Web / Natural Language",
                "reproducibility_token": None,
                "claimant": {"name": "Policyholder", "email": "user@example.com", "phone": ""},
                "claim_details": {"policy_number": "POL-HEALTH-GOLD-2026", "claim_type": "Health", "amount": 50000.0, "description": query},
                "query": query,
                "decomposed_tasks": [],
                "routing_plan": None,
                "episodic_memory": [],
                "long_term_memory": {},
                "documents": [],
                "extracted_document_data": {},
                "policy_context": [],
                "policy_verification": {},
                "risk_analysis": {},
                "assessment": {},
                "audit_events": [],
                "mcp_tool_calls": [],
                "messages": [],
                "current_agent": "SupervisorAgent",
                "confidence": 0.90,
                "requires_human_review": False,
                "human_review_reason": None,
                "guardrail_result": {},
                "output_guardrail_result": None,
                "evaluation_data": None,
                "cost_data": None,
                "governance_data": None,
                "final_response": None,
                "notifications_dispatched": [],
                "errors": []
            }
            final_res = process_claim_graph(init_state)
            return {
                "answer": final_res.get("final_response", ""),
                "claim_id": c_id,
                "requires_human_review": final_res.get("requires_human_review", False),
                "sources": [c.get("source_doc", "Policy Knowledge Base") for c in final_res.get("policy_context", [])],
                "confidence": final_res.get("confidence", 0.90),
                "evaluation_data": final_res.get("evaluation_data"),
                "cost_data": final_res.get("cost_data")
            }

    def process_claim(self, claim_payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            with httpx.Client(timeout=60.0) as client:
                res = client.post(f"{self.base_url}/api/claims/process", json=claim_payload)
                if res.status_code == 200:
                    return res.json()
                return {"error": res.text, "status_code": res.status_code}
        except Exception as e:
            logger.info(f"Direct in-process claim execution fallback: {e}")
            from backend.graph.workflow import process_claim_graph
            import uuid
            c_id = claim_payload.get("claim_id") or f"CLM-{uuid.uuid4().hex[:6].upper()}"
            init_state = {
                "claim_id": c_id,
                "trace_id": f"TRC-{uuid.uuid4().hex[:8].upper()}",
                "persona": claim_payload.get("persona", "Claimant"),
                "channel": claim_payload.get("channel", "Web App (Streamlit)"),
                "reproducibility_token": None,
                "claimant": claim_payload.get("claimant", {}),
                "claim_details": claim_payload.get("claim_details", {}),
                "query": None,
                "decomposed_tasks": [],
                "routing_plan": None,
                "episodic_memory": [],
                "long_term_memory": {},
                "documents": claim_payload.get("documents", []),
                "extracted_document_data": {},
                "policy_context": [],
                "policy_verification": {},
                "risk_analysis": {},
                "assessment": {},
                "audit_events": [],
                "mcp_tool_calls": [],
                "messages": [],
                "current_agent": "START",
                "confidence": 0.85,
                "requires_human_review": False,
                "human_review_reason": None,
                "guardrail_result": {},
                "output_guardrail_result": None,
                "evaluation_data": None,
                "cost_data": None,
                "governance_data": None,
                "final_response": None,
                "notifications_dispatched": [],
                "errors": []
            }
            final_res = process_claim_graph(init_state)
            return {
                "claim_id": c_id,
                "status": "Requires Human Review" if final_res.get("requires_human_review") else "Completed",
                "summary": f"Adjudicated claim for {claim_payload.get('claimant', {}).get('name', 'Policyholder')}.",
                "assessment": final_res.get("assessment", {}),
                "risk_analysis": final_res.get("risk_analysis", {}),
                "policy_verification": final_res.get("policy_verification", {}),
                "explanation": final_res.get("final_response", ""),
                "audit_events": final_res.get("audit_events", []),
                "requires_human_review": final_res.get("requires_human_review", False),
                "human_review_reason": final_res.get("human_review_reason"),
                "guardrails": final_res.get("guardrail_result", {})
            }

    def get_claim(self, claim_id: str) -> Optional[Dict[str, Any]]:
        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.get(f"{self.base_url}/api/claims/{claim_id}")
                if res.status_code == 200:
                    return res.json()
        except Exception as e:
            logger.info(f"Direct in-process claim lookup fallback: {e}")
            from backend.services.claim_service import ClaimService
            rec = ClaimService.get_claim_by_id(claim_id)
            return rec.model_dump() if rec else None
        return None

    def get_audit_trail(self, claim_id: str) -> List[Dict[str, Any]]:
        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.get(f"{self.base_url}/api/audit/{claim_id}")
                if res.status_code == 200:
                    return res.json()
        except Exception as e:
            logger.info(f"Direct in-process audit lookup fallback: {e}")
            from backend.services.audit_service import AuditService
            events = AuditService.get_claim_audit_trail(claim_id)
            return [e.model_dump() for e in events]
        return []

    def get_governance_overview(self) -> Dict[str, Any]:
        return {
            "data_governance": GovernanceService.get_data_governance_report(),
            "bias_fairness": GovernanceService.evaluate_fairness(),
            "model_governance": GovernanceService.get_model_governance_report(),
            "compliance_matrix": GovernanceService.get_regulatory_compliance_matrix()
        }

    def run_adversarial_test(self) -> Dict[str, Any]:
        return GovernanceService.run_adversarial_test_suite()

    def get_cost_analysis(self) -> Dict[str, Any]:
        return CostService.get_aggregate_cost_metrics()

    def get_observability(self) -> Dict[str, Any]:
        return ObservabilityService.get_dashboard_telemetry()

    def get_compliance_report(self) -> Dict[str, Any]:
        return ObservabilityService.generate_automated_compliance_report()

    def list_mcp_tools(self) -> List[Dict[str, Any]]:
        """Returns registered 10 MCP tools catalog."""
        return self.mcp.list_available_tools().get("tools", [])

    def execute_mcp_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a registered MCP tool."""
        return self.mcp.call_tool(tool_name, args)

    def query_knowledge_graph(self, term: str = "") -> List[Dict[str, str]]:
        """Queries the Layer 3 Knowledge Graph."""
        if term:
            return MemoryService.query_knowledge_graph(term)
        return MemoryService.get_all_graph_triples()

    def get_gnotheia_sample_claims(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Reads sample polycontext claims from GNOTHEIA Parquet dataset."""
        gnotheia_path = os.path.join(os.path.dirname(__file__), "..", "data", "claims", "GNOTHEIA", "data.parquet")
        if os.path.exists(gnotheia_path):
            try:
                import pandas as pd
                df = pd.read_parquet(gnotheia_path)
                sample = df.head(limit).to_dict(orient="records")
                return [{
                    "id": str(r.get("id")),
                    "note": str(r.get("note", ""))[:120] + "...",
                    "has_polycontext_data": bool(r.get("data")),
                    "dataset": "GNOTHEIA SBVR Synthetic Claims"
                } for r in sample]
            except Exception as e:
                logger.warning(f"Error reading GNOTHEIA parquet: {e}")
        return []

    def record_feedback(self, claim_id: str, role: str, rating: int, comment: str) -> Dict[str, Any]:
        return ObservabilityService.record_user_feedback(claim_id, role, rating, comment)


insuragent_client = InsurAgentClient()
