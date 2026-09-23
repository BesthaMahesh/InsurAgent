"""
Layer 2: Orchestration & Control Plane (LangGraph)
Typed Agent State flowing across all nodes in the LangGraph orchestration pipeline.
Includes Goal Decomposition, Memory contexts (Episodic & Long-term), Tool execution traces, and Persona context.
"""
from typing import List, Dict, Any, Optional, TypedDict, Annotated
import operator


class AgentState(TypedDict):
    """
    Typed Agent State flowing across all nodes in the LangGraph orchestration pipeline.
    Enriched with full architectural layers:
    1. Multi-Channel Persona Context
    2. Orchestrator Goal Decomposition & Plan
    3. Episodic & Long-Term Memory
    4. 6 Specialized Agent Outputs
    5. MCP Tool Execution Logs
    6. Observability, Cost, Evaluation & Governance
    """
    # Identifiers & Persona Context
    claim_id: str
    trace_id: str
    persona: Optional[str]  # Claimant, Employee, Partner
    channel: Optional[str]  # Web, Mobile, Chat/Voice, API
    reproducibility_token: Optional[str]
    claimant: Dict[str, Any]
    claim_details: Dict[str, Any]
    query: Optional[str]
    
    # Layer 2: Orchestrator Goal Understanding & Task Decomposition
    decomposed_tasks: Optional[List[Dict[str, Any]]]
    routing_plan: Optional[str]
    
    # Layer 3: Knowledge & Memory Layer
    episodic_memory: Optional[List[Dict[str, Any]]]
    long_term_memory: Optional[Dict[str, Any]]
    policy_context: List[Dict[str, Any]]
    
    # Layer 4: 6 Domain Experts Working Together
    # 1. Claim Intake Agent
    intake_data: Optional[Dict[str, Any]]
    # 2. Document Analysis Agent
    documents: List[Dict[str, Any]]
    extracted_document_data: Dict[str, Any]
    # 3. Policy Verification Agent
    policy_verification: Dict[str, Any]
    # 4. Fraud / Risk Analysis Agent
    risk_analysis: Dict[str, Any]
    # 5. Claim Assessment Agent
    assessment: Dict[str, Any]
    # 6. Audit & Compliance Agent
    audit_events: Annotated[List[Dict[str, Any]], operator.add]
    
    # Layer 5: MCP Tool Logs
    mcp_tool_calls: Optional[List[Dict[str, Any]]]
    
    # Control Plane, Routing & HITL
    messages: List[Dict[str, Any]]
    current_agent: str
    confidence: float
    requires_human_review: bool
    human_review_reason: Optional[str]
    
    # Layer 7: Guardrails & Governance
    guardrail_result: Dict[str, Any]
    output_guardrail_result: Optional[Dict[str, Any]]
    governance_data: Optional[Dict[str, Any]]
    
    # Layer 6: Observability, Cost & Evaluation
    evaluation_data: Optional[Dict[str, Any]]
    cost_data: Optional[Dict[str, Any]]
    
    # Final Output & Notifications
    final_response: Optional[str]
    notifications_dispatched: Optional[List[Dict[str, Any]]]
    errors: Annotated[List[str], operator.add]
