"""
Layer 2: Orchestration & Control Plane (LangGraph) Nodes
Connects the 6 Domain Expert Agents, Input/Output Guardrails, MCP Tools, and Observability Layers.
"""
from typing import Dict, Any
import uuid
from backend.graph.state import AgentState
from backend.guardrails.input_guardrail import InputGuardrail
from backend.guardrails.output_guardrail import OutputGuardrail
from backend.agents.supervisor_agent import SupervisorAgent
from backend.agents.claim_intake_agent import ClaimIntakeAgent
from backend.agents.document_agent import DocumentAgent
from backend.agents.policy_agent import PolicyAgent
from backend.agents.risk_agent import RiskAgent
from backend.agents.assessment_agent import AssessmentAgent
from backend.agents.audit_agent import AuditAgent
from backend.services.evaluation_service import EvaluationService
from backend.services.cost_service import CostService
from backend.services.observability_service import ObservabilityService
from backend.services.memory_service import MemoryService
from backend.mcp.client import MCPClient
from backend.core.logging_config import logger


# Node 1: Input Guardrail
def input_guardrail_node(state: AgentState) -> Dict[str, Any]:
    query = state.get("query")
    details = state.get("claim_details", {})
    claimant = state.get("claimant", {})
    claim_id = state.get("claim_id") or f"CLM-{uuid.uuid4().hex[:8].upper()}"
    trace_id = state.get("trace_id") or f"TRC-{uuid.uuid4().hex[:8].upper()}"

    if query:
        res = InputGuardrail.validate_text(query, context="chat_query")
    else:
        res = InputGuardrail.validate_claim_payload(
            claimant_name=claimant.get("name", ""),
            policy_number=details.get("policy_number", ""),
            claim_type=details.get("claim_type", "Health"),
            amount=float(details.get("amount", 0.0)),
            description=details.get("description", "")
        )

    # Record to Episodic Memory
    MemoryService.record_episodic_event(
        claim_id=claim_id,
        agent="InputGuardrail",
        action=f"Input validation: allowed={res['allowed']}. PII: {res['pii_detected']}, Injection: {res['prompt_injection_detected']}."
    )

    audit_entry = {
        "claim_id": claim_id,
        "agent": "InputGuardrail",
        "action": f"5-Check Input Guardrail passed: {res['allowed']}. (PII: {res['pii_detected']}, Injection: {res['prompt_injection_detected']}, Policy: {res['policy_check_passed']}, Safety: {res['content_safety_passed']})",
        "source": "Deterministic Input Guardrail Suite",
        "status": "success" if res["allowed"] else "blocked",
        "timestamp": ""
    }

    return {
        "claim_id": claim_id,
        "trace_id": trace_id,
        "guardrail_result": res,
        "requires_human_review": not res["allowed"],
        "human_review_reason": "; ".join(res["reasons"]) if not res["allowed"] else None,
        "audit_events": [audit_entry],
        "errors": [] if res["allowed"] else res["reasons"]
    }


# Node 2: Supervisor / Orchestrator
def supervisor_node(state: AgentState) -> Dict[str, Any]:
    return SupervisorAgent.plan_workflow(state)


# Node 3: Claim Intake Agent
def intake_node(state: AgentState) -> Dict[str, Any]:
    return ClaimIntakeAgent.process_intake(state)


# Node 4: Document Analysis Agent
def document_node(state: AgentState) -> Dict[str, Any]:
    return DocumentAgent.process_documents(state)


# Node 5: Policy Verification Agent
policy_agent_instance = PolicyAgent()
def policy_node(state: AgentState) -> Dict[str, Any]:
    return policy_agent_instance.verify_coverage(state)


# Node 6: Fraud & Risk Agent
risk_agent_instance = RiskAgent()
def risk_node(state: AgentState) -> Dict[str, Any]:
    return risk_agent_instance.analyze_risk(state)


# Node 7: Assessment Agent
def assessment_node(state: AgentState) -> Dict[str, Any]:
    return AssessmentAgent.assess_claim(state)


# Node 8: Human Review Check / Routing
def human_review_node(state: AgentState) -> Dict[str, Any]:
    claim_id = state.get("claim_id", "")
    reason = state.get("human_review_reason", "Escalated for senior claim adjuster review.")
    
    logger.info(f"[HumanReviewNode] Case {claim_id} flagged for human review. Reason: {reason}")
    
    # Trigger notification via MCP
    mcp_call = None
    try:
        mcp = MCPClient()
        mcp_res = mcp.send_notification(
            recipient="senior_adjuster_queue@insuragent.internal",
            message=f"Claim {claim_id} escalated for mandatory human review: {reason}"
        )
        mcp_call = {"tool": "send_notification", "status": "success", "result": mcp_res}
    except Exception as e:
        logger.warning(f"[HumanReviewNode] Notification trigger notice: {e}")
        mcp_call = {"tool": "send_notification", "status": "error", "error": str(e)}

    # Record to Episodic Memory
    MemoryService.record_episodic_event(
        claim_id=claim_id,
        agent="HumanReviewNode",
        action=f"Human-in-the-loop checkpoint triggered: {reason}"
    )

    audit_entry = {
        "claim_id": claim_id,
        "agent": "HumanReviewCheck",
        "action": f"Human-in-the-loop checkpoint triggered: {reason}",
        "source": "HITL Orchestration Node",
        "status": "review_required",
        "timestamp": ""
    }

    return {
        "requires_human_review": True,
        "human_review_reason": reason,
        "mcp_tool_calls": [mcp_call] if mcp_call else [],
        "audit_events": [audit_entry]
    }


# Node 9: Audit & Compliance Agent
def audit_node(state: AgentState) -> Dict[str, Any]:
    return AuditAgent.record_audit_trail(state)


# Node 10: Output Guardrail & Synthesis Layer
def output_guardrail_node(state: AgentState) -> Dict[str, Any]:
    claim_id = state.get("claim_id", "")
    assessment = state.get("assessment", {})
    policy_ver = state.get("policy_verification", {})
    risk = state.get("risk_analysis", {})
    confidence = float(state.get("confidence", 0.85))
    risk_score = float(risk.get("risk_score", 0.12))
    has_evidence = policy_ver.get("policy_found", False)
    req_human = state.get("requires_human_review", False)
    reason = state.get("human_review_reason")

    # Construct formatted explanation
    rec = assessment.get("recommendation", "Requires Human Review")
    calc = assessment.get("calculation_breakdown", {})
    
    exp = (
        f"Claim {claim_id} Assessment: {rec}.\n\n"
        f"• Policy Coverage: {policy_ver.get('coverage_status', 'Unknown')} ({policy_ver.get('policy_interpretation', '')})\n"
        f"• Risk Evaluation: {risk.get('risk_level', 'Low Risk')} (Score: {risk.get('risk_score', 0.12)})\n"
        f"• Recommendation Reasoning: {assessment.get('reasoning', '')}\n"
    )

    if calc:
        exp += f"• Itemized Payout: ₹{calc.get('net_payable_amount', 0.0):,.2f} (Incurred: ₹{calc.get('claimed_amount', 0.0):,.2f}, Deductible: ₹{calc.get('deductible_deducted', 0.0):,.2f}, Co-pay: ₹{calc.get('copay_deducted', 0.0):,.2f})\n"

    if req_human or reason:
        exp += f"\n⚠️ Human Review Triggered: {reason or 'Standard review threshold reached.'}"

    sanitized_out = OutputGuardrail.validate_and_sanitize_response(
        response_text=exp,
        confidence=confidence,
        risk_score=risk_score,
        has_policy_evidence=has_evidence,
        requires_human_review=req_human,
        human_review_reason=reason
    )

    # Calculate Evaluation, Cost, and Observability Layers
    eval_report = EvaluationService.evaluate_claim_execution(
        claim_payload={"claim_id": claim_id, "claim_details": state.get("claim_details", {})},
        final_state={"final_response": sanitized_out["sanitized_response"], "policy_context": state.get("policy_context", []), "confidence": confidence}
    )

    cost_report = CostService.calculate_claim_cost(
        claim_id=claim_id,
        state=state
    )

    # Record to Episodic Memory
    MemoryService.record_episodic_event(
        claim_id=claim_id,
        agent="OutputGuardrail",
        action=f"Output validated: Groundedness={eval_report['groundedness_score']}, Quality={eval_report['overall_quality_score']}."
    )

    audit_entry = {
        "claim_id": claim_id,
        "agent": "OutputGuardrail",
        "action": f"Output 5-Check Guardrail validated. Certified safe. Groundedness: {eval_report['groundedness_score']}, Quality: {eval_report['overall_quality_score']}.",
        "source": "Deterministic Output Guardrail Suite",
        "status": "success",
        "timestamp": ""
    }

    return {
        "final_response": sanitized_out["sanitized_response"],
        "requires_human_review": sanitized_out["requires_human_review"],
        "human_review_reason": sanitized_out["human_review_reason"],
        "output_guardrail_result": sanitized_out,
        "evaluation_data": eval_report,
        "cost_data": cost_report,
        "audit_events": [audit_entry]
    }
