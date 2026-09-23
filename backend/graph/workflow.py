from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from backend.graph.state import AgentState
from backend.graph.nodes import (
    input_guardrail_node,
    supervisor_node,
    intake_node,
    document_node,
    policy_node,
    risk_node,
    assessment_node,
    audit_node,
    human_review_node,
    output_guardrail_node
)
from backend.core.logging_config import logger


def route_after_input_guardrail(state: AgentState) -> str:
    """Checks if input guardrails allowed the request."""
    guardrail_res = state.get("guardrail_result", {})
    if not guardrail_res.get("allowed", True):
        logger.warning(f"Input Guardrail blocked request: {guardrail_res.get('reasons')}")
        return "human_review"
    return "supervisor"


def route_after_assessment(state: AgentState) -> str:
    """Evaluates whether to branch to human review or proceed directly to audit."""
    requires_human = state.get("requires_human_review", False)
    confidence = float(state.get("confidence", 1.0))
    risk_data = state.get("risk_analysis", {})
    risk_score = float(risk_data.get("risk_score", 0.0))

    if requires_human or confidence < 0.75 or risk_score >= 0.60:
        return "human_review"
    return "audit"


def create_claim_workflow() -> Any:
    """Constructs and compiles the full LangGraph claim processing workflow."""
    workflow = StateGraph(AgentState)

    # 1. Add all nodes
    workflow.add_node("input_guardrail", input_guardrail_node)
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("intake", intake_node)
    workflow.add_node("document", document_node)
    workflow.add_node("policy", policy_node)
    workflow.add_node("risk", risk_node)
    workflow.add_node("assessment", assessment_node)
    workflow.add_node("human_review", human_review_node)
    workflow.add_node("audit", audit_node)
    workflow.add_node("output_guardrail", output_guardrail_node)

    # 2. Define standard sequential edges and conditional routing
    workflow.add_edge(START, "input_guardrail")

    workflow.add_conditional_edges(
        "input_guardrail",
        route_after_input_guardrail,
        {
            "supervisor": "supervisor",
            "human_review": "human_review"
        }
    )

    workflow.add_edge("supervisor", "intake")
    workflow.add_edge("intake", "document")
    workflow.add_edge("document", "policy")
    workflow.add_edge("policy", "risk")
    workflow.add_edge("risk", "assessment")

    workflow.add_conditional_edges(
        "assessment",
        route_after_assessment,
        {
            "human_review": "human_review",
            "audit": "audit"
        }
    )

    workflow.add_edge("human_review", "audit")
    workflow.add_edge("audit", "output_guardrail")
    workflow.add_edge("output_guardrail", END)

    # 3. Compile runnable graph
    return workflow.compile()


# Singleton compiled graph instance
claim_workflow_app = create_claim_workflow()


def process_claim_graph(initial_state: Dict[str, Any]) -> Dict[str, Any]:
    """Helper function to execute state through compiled workflow graph."""
    logger.info(f"Initiating LangGraph execution for claim: {initial_state.get('claim_id')}")
    final_state = claim_workflow_app.invoke(initial_state)
    logger.info(f"LangGraph execution finished for claim: {initial_state.get('claim_id')}")
    return final_state
