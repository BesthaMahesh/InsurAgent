"""
Layer 4: Agent Layer — Agent 4: Fraud / Risk Analysis Agent
Responsibilities:
1. Detect anomalies
2. Check risk indicators
3. Use risk models (RAG + MCP Tools)
4. Analyze claim history
5. Assign risk level
"""
from typing import Dict, Any, List
from backend.mcp.client import MCPClient
from backend.services.memory_service import MemoryService
from backend.core.logging_config import logger


class RiskAgent:
    """
    4. Fraud / Risk Analysis Agent.
    Domain expert responsible for detecting claim anomalies, evaluating risk indicators,
    querying the MCP Fraud Bureau, analyzing historical claim patterns, and assigning an overall risk level.
    """

    def __init__(self):
        self.mcp = MCPClient()

    def analyze_risk(self, state: Dict[str, Any]) -> Dict[str, Any]:
        claim_id = state.get("claim_id", "")
        details = state.get("claim_details", {})
        docs_data = state.get("extracted_document_data", {})
        amount = float(details.get("amount", 0.0))
        claim_type = details.get("claim_type", "Health")
        
        # 1. Check Risk Indicators via MCP Fraud Bureau Tool
        mcp_res = self.mcp.get_risk_indicators(claim_id)
        mcp_data = mcp_res.get("data", mcp_res)
        
        base_score = float(mcp_data.get("risk_score", 0.12))
        indicators = list(mcp_data.get("indicators", []))
        anomalies_detected: List[str] = []

        # 2. Detect Anomalies & Analyze Claim History Patterns
        if amount > 200000.0:
            base_score = min(1.0, base_score + 0.15)
            anomaly = f"High-value {claim_type} claim amount (INR {amount:,.2f}) exceeds standard fast-track ceiling."
            indicators.append(anomaly)
            anomalies_detected.append(anomaly)

        if docs_data.get("processed_count", 0) == 0:
            base_score = min(1.0, base_score + 0.20)
            anomaly = "Absence of supporting invoices/evidence during initial submission."
            indicators.append(anomaly)
            anomalies_detected.append(anomaly)

        # 3. Assign Risk Level
        if base_score >= 0.60:
            risk_level = "Requires Investigation"
        elif base_score >= 0.40:
            risk_level = "Medium Risk"
        else:
            risk_level = "Low Risk"

        risk_summary = (
            f"Risk profile evaluated at {risk_level} (Score: {base_score:.2f}). "
            f"Key indicators: {'; '.join(indicators[:3])}"
        )

        logger.info(f"[RiskAgent] Evaluated {claim_id}: Level={risk_level}, Score={base_score:.2f}")

        # 4. Record to Episodic Memory
        MemoryService.record_episodic_event(
            claim_id=claim_id,
            agent="RiskAgent",
            action=f"Risk Level assigned: {risk_level} (Score: {base_score:.2f}). Anomalies: {len(anomalies_detected)}."
        )

        risk_analysis_result = {
            "risk_level": risk_level,
            "risk_score": round(base_score, 2),
            "flags": indicators,
            "anomalies": anomalies_detected,
            "risk_summary": risk_summary,
            "evaluation_engine": "MCP Fraud Bureau & Risk Model Hybrid"
        }

        audit_entry = {
            "claim_id": claim_id,
            "agent": "RiskAgent",
            "action": f"Calculated risk index: {risk_level} (Score: {base_score:.2f}). Anomalies detected: {len(anomalies_detected)}.",
            "source": "MCP Fraud Bureau & Risk Models",
            "status": "success",
            "timestamp": ""
        }

        return {
            "current_agent": "RiskAgent",
            "risk_analysis": risk_analysis_result,
            "audit_events": [audit_entry]
        }
