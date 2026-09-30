"""
Processing Workflow View for InsurAgent enterprise UI.
Presents the claim adjudication journey in clear, client-friendly business terminology
with expandable technical architecture details for engineering and compliance review.
"""
import streamlit as st
import textwrap
from frontend.components.workflow import render_workflow_diagram
from frontend.components.agent_status import render_agent_card


def render_workflow_view() -> None:
    st.markdown('<div class="page-title">Processing Workflow</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">End-to-end claim adjudication journey orchestrating autonomous specialized agents with deterministic guardrails.</div>', unsafe_allow_html=True)

    # 1. Visual Claim Processing Journey
    render_workflow_diagram()

    st.write("")

    # 2. 6 Specialized Collaborative Workers Registry
    st.markdown("##### 🤖 Specialized Collaborative Agents Registry")

    # Supervisor
    render_agent_card(
        agent_name="Supervisor / Orchestrator Agent",
        purpose="Task Decomposition, Routing Plan Formulation & State Memory Management",
        status="Healthy",
        execution_time_ms=145,
        tools_used="LangGraph State Engine, Memory Manager",
        input_desc="Claim Submission Payload or Natural Language Query",
        output_desc="Decomposed Execution Plan with 7 Sequenced Subtasks",
        confidence=1.00
    )

    # 1. Claim Intake Agent
    render_agent_card(
        agent_name="1. Claim Intake Agent",
        purpose="Classifies line of business, normalizes claimant entities, and checks record completeness",
        status="Completed",
        execution_time_ms=180,
        tools_used="Intake Validation Rules, Entity Normalizer",
        input_desc="Claimant Profile, Policy Number, Incident Particulars",
        output_desc="Normalized Claim JSON with Completeness Score (100%)",
        confidence=0.98
    )

    # 2. Document Analysis Agent
    render_agent_card(
        agent_name="2. Document Analysis Agent",
        purpose="Performs computer vision OCR, parses itemized invoices, and checks document consistency",
        status="Completed",
        execution_time_ms=420,
        tools_used="Vision-OCR Engine, Invoice Parser",
        input_desc="Base64 Document Byte Streams (PDF/Images)",
        output_desc="Extracted Table Entities, Invoice Totals & Validation Flags",
        confidence=0.95
    )

    # 3. Policy Verification Agent
    render_agent_card(
        agent_name="3. Policy Verification Agent",
        purpose="Retrieves relevant policy clauses from ChromaDB RAG, validates eligibility, waiting periods, and exclusions",
        status="Completed",
        execution_time_ms=680,
        tools_used="ChromaDB Vector Store, all-MiniLM-L6-v2",
        input_desc="Claim Line, Incident Description, Policy Identifier",
        output_desc="Retrieved Grounded Policy Clauses (Coverage: Covered)",
        confidence=0.91
    )

    # 4. Fraud / Risk Analysis Agent
    render_agent_card(
        agent_name="4. Fraud / Risk Analysis Agent",
        purpose="Evaluates anomaly indicators, loss ratios, and calls MCP Fraud Bureau",
        status="Completed",
        execution_time_ms=310,
        tools_used="MCP Fraud Bureau API, Anomaly Rules Engine",
        input_desc="Claim ID, Incurred Amount, Provider Geolocation",
        output_desc="Risk Index Score: 0.12 (Low Risk), Zero Anomaly Flags",
        confidence=0.94
    )

    # 5. Claim Assessment Agent
    render_agent_card(
        agent_name="5. Claim Assessment Agent",
        purpose="Synthesizes findings, computes itemized deductible/co-pay payouts, and determines HITL review need",
        status="Completed",
        execution_time_ms=550,
        tools_used="Synthesized Multi-Agent Adjudication Engine",
        input_desc="Intake Data, Policy Clauses, OCR Invoices, Risk Profile",
        output_desc="Recommendation: Approved, Net Payable: ₹1,20,000",
        confidence=0.90
    )

    # 6. Audit & Compliance Agent
    render_agent_card(
        agent_name="6. Audit & Compliance Agent",
        purpose="Generates immutable audit trail, verifies IRDAI/GDPR regulatory compliance, and stamps cryptographic token",
        status="Completed",
        execution_time_ms=120,
        tools_used="SQLite Audit Store, SHA-256 Hasher",
        input_desc="Chronological Audit Events from all Nodes",
        output_desc="Sealed Audit Trace (Token: A7F43E2910BC), IRDAI Certified",
        confidence=1.00
    )

    st.write("")

    # 3. Expandable Technical Architecture Details
    with st.expander("🛠️ View Technical Architecture Details (LangGraph & Control Plane)"):
        st.markdown(textwrap.dedent("""
        <div style="font-size:12.5px; line-height:1.6; color:#334155;">
            <b>Orchestration Engine:</b> LangGraph v0.2.x Stateful Graph Engine<br>
            <b>State Schema:</b> <code>AgentState</code> TypedDict capturing 28 distinct workflow fields including <code>reproducibility_token</code>, <code>episodic_memory</code>, and <code>guardrail_result</code>.<br>
            <b>Conditional Routing:</b> Deterministic branching routes to <code>HumanReviewNode</code> if <code>confidence &lt; 0.75</code> or <code>risk_score &gt; 0.40</code>.<br>
            <b>Integration Protocol:</b> Model Context Protocol (MCP) tool standard for external core insurance systems.
        </div>
        """), unsafe_allow_html=True)
