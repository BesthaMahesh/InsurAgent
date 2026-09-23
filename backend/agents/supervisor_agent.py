"""
Layer 2: Orchestration & Control Plane (LangGraph)
Supervisor / Orchestrator Agent Runtime:
- Goal Understanding & Task Decomposition
- Agent Planning & Routing
- Memory Management (Episodic & Long-term Context)
- Tool Routing & Policy Guardrail Coordination
"""
from typing import Dict, Any, List
from backend.services.memory_service import MemoryService
from backend.core.logging_config import logger


class SupervisorAgent:
    """
    Supervisor / Orchestrator Agent.
    Plans, schedules, decomposes goals, and injects memory context across the multi-agent graph.
    """

    @staticmethod
    def plan_workflow(state: Dict[str, Any]) -> Dict[str, Any]:
        """Inspects incoming claim/query, decomposes goals, and loads memory context."""
        claim_id = state.get("claim_id", "UNKNOWN")
        claimant = state.get("claimant", {})
        details = state.get("claim_details", {})
        is_chat_query = bool(state.get("query"))
        customer_id = claimant.get("customer_id", "CUST-001")

        logger.info(f"[SupervisorAgent] Goal Understanding & Task Decomposition for {claim_id} (is_chat={is_chat_query})")

        # 1. Goal Understanding & Task Decomposition
        if is_chat_query:
            decomposed_tasks = [
                {"task_id": "T1", "agent": "PolicyAgent", "objective": "Retrieve grounded policy clauses from Knowledge RAG", "status": "pending"},
                {"task_id": "T2", "agent": "AuditAgent", "objective": "Log query and seal audit trace", "status": "pending"},
                {"task_id": "T3", "agent": "OutputGuardrail", "objective": "Apply safety, groundedness, and explainability guardrails", "status": "pending"}
            ]
            routing_plan = "Natural Language Knowledge Retrieval & Adjudication Query"
        else:
            decomposed_tasks = [
                {"task_id": "T1", "agent": "ClaimIntakeAgent", "objective": "Classify claim type and validate field completeness", "status": "pending"},
                {"task_id": "T2", "agent": "DocumentAgent", "objective": "Perform OCR extraction and validate invoice completeness", "status": "pending"},
                {"task_id": "T3", "agent": "PolicyAgent", "objective": "Verify policy eligibility, waiting periods, and exclusions via ChromaDB RAG", "status": "pending"},
                {"task_id": "T4", "agent": "RiskAgent", "objective": "Evaluate anomaly indicators via MCP Fraud Bureau", "status": "pending"},
                {"task_id": "T5", "agent": "AssessmentAgent", "objective": "Synthesize adjudication decision, itemize payouts, and evaluate HITL need", "status": "pending"},
                {"task_id": "T6", "agent": "AuditAgent", "objective": "Generate immutable audit trail and IRDAI compliance stamp", "status": "pending"},
                {"task_id": "T7", "agent": "OutputGuardrail", "objective": "Sanitize response, verify groundedness, and compute cost/observability telemetry", "status": "pending"}
            ]
            routing_plan = "End-to-End Multi-Agent Collaborative Claim Adjudication Pipeline"

        # 2. Memory Context Management
        user_long_term = MemoryService.get_long_term_context(f"user:{customer_id}") or {}
        domain_rules = MemoryService.get_long_term_context("domain:health_deductibles") or {}
        episodic_history = MemoryService.get_episodic_history(claim_id)

        combined_long_term = {
            "user_profile": user_long_term,
            "domain_rules": domain_rules,
            "loaded_at": "SupervisorAgent"
        }

        # 3. Record Supervisor event in episodic memory
        MemoryService.record_episodic_event(
            claim_id=claim_id,
            agent="SupervisorAgent",
            action=f"Decomposed goal into {len(decomposed_tasks)} tasks. Plan: {routing_plan}."
        )

        audit_entry = {
            "claim_id": claim_id,
            "agent": "SupervisorAgent",
            "action": f"Task decomposition completed ({len(decomposed_tasks)} subtasks). Orchestrator Routing: {routing_plan}.",
            "source": "LangGraph Orchestrator & Control Plane",
            "status": "success",
            "timestamp": ""
        }

        return {
            "current_agent": "SupervisorAgent",
            "decomposed_tasks": decomposed_tasks,
            "routing_plan": routing_plan,
            "episodic_memory": episodic_history,
            "long_term_memory": combined_long_term,
            "messages": [
                {
                    "role": "system",
                    "content": f"LangGraph Orchestrator initialized. Plan: {routing_plan}."
                }
            ],
            "audit_events": [audit_entry]
        }
