"""
Processing Workflow View for InsurAgent enterprise UI.
Presents the Claim Processing Journey in a clean, uncluttered business layout
with expandable Technical Processing Details for full architectural transparency.
"""
import streamlit as st
from frontend.styles import render_html


def render_workflow_view() -> None:
    st.markdown('<div class="page-title">Claim Processing Journey</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Track how your claim moves through intake verification, document analysis, policy coverage check, risk assessment, and audit sealing.</div>', unsafe_allow_html=True)

    # 1. Top Journey Summary Card
    journey_header_html = """
    <div class="enterprise-card" style="margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding-bottom:10px; margin-bottom:12px;">
            <div>
                <div class="card-title">Autonomous Adjudication Lifecycle</div>
                <div class="card-subtitle" style="margin-bottom:0;">Continuous 8-stage verification pipeline with automated straight-through execution.</div>
            </div>
            <span class="status-badge badge-green">● Route: Straight-Through Adjudication</span>
        </div>
    </div>
    """
    render_html(journey_header_html)

    # 2. 8-Stage Clean Grid (2 rows of 4 columns to avoid horizontal overflow on smaller screens)
    stages = [
        ("1", "Claim Received", "Intake payload captured & parsed", "Completed", "badge-green"),
        ("2", "Information Verified", "Entity records & policy validity checked", "Completed", "badge-green"),
        ("3", "Documents Reviewed", "Vision-OCR extracted & invoices verified", "Completed", "badge-green"),
        ("4", "Coverage Verified", "Policy terms & limits retrieved via RAG", "Completed", "badge-purple"),
        ("5", "Risk Assessed", "Anomaly indicators & bureau flags evaluated", "Completed", "badge-green"),
        ("6", "Claim Evaluated", "Itemized deduction & net payout calculated", "Completed", "badge-blue"),
        ("7", "Human Review", "Automated checkpoint / Adjuster queue", "Straight-Through", "badge-green"),
        ("8", "Finalized & Audited", "Immutable audit seal & token generated", "Certified", "badge-green")
    ]

    st.markdown("##### 📍 Claim Processing Stages")
    
    # Row 1: Stages 1 to 4
    r1_cols = st.columns(4)
    for idx, (num, title, desc, status_text, badge_cls) in enumerate(stages[:4]):
        with r1_cols[idx]:
            card_html = f"""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:14px 12px; margin-bottom:10px; min-height:120px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="width:22px; height:22px; border-radius:50%; background:#0284c7; color:#ffffff; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:800;">{num}</span>
                    <span class="status-badge {badge_cls}">{status_text}</span>
                </div>
                <div style="font-size:13px; font-weight:750; color:#0f172a; margin-top:6px; line-height:1.2;">{title}</div>
                <div style="font-size:11px; color:#64748b; margin-top:2px;">{desc}</div>
            </div>
            """
            render_html(card_html)

    # Row 2: Stages 5 to 8
    r2_cols = st.columns(4)
    for idx, (num, title, desc, status_text, badge_cls) in enumerate(stages[4:]):
        with r2_cols[idx]:
            card_html = f"""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:14px 12px; margin-bottom:10px; min-height:120px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="width:22px; height:22px; border-radius:50%; background:#0284c7; color:#ffffff; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:800;">{num}</span>
                    <span class="status-badge {badge_cls}">{status_text}</span>
                </div>
                <div style="font-size:13px; font-weight:750; color:#0f172a; margin-top:6px; line-height:1.2;">{title}</div>
                <div style="font-size:11px; color:#64748b; margin-top:2px;">{desc}</div>
            </div>
            """
            render_html(card_html)

    st.write("")

    # 3. Expandable Technical Processing Details (Preserving full architectural depth)
    with st.expander("🛠️ View Technical Processing Details (Multi-Agent Control Plane)"):
        st.markdown("<div style='font-size:12.5px; color:#64748b; margin-bottom:12px;'>Inspect specialized collaborative agents, underlying tools, state schema, and execution latencies.</div>", unsafe_allow_html=True)

        agents = [
            ("Supervisor / Orchestrator Agent", "Goal Understanding, Task Decomposition, Tool Routing & Memory Context Management", "145 ms", "LangGraph State Engine, Memory Manager", "Raw Claim Payload", "Decomposed Execution Plan (7 Subtasks)", "100%"),
            ("1. Claim Intake Agent", "Classifies line of business, normalizes entity fields, and validates record completeness", "180 ms", "Intake Validation Rules, Entity Normalizer", "Claimant Profile, Policy Number, Incident Particulars", "Normalized Claim JSON (100% Completeness)", "98%"),
            ("2. Document Analysis Agent", "Performs computer vision OCR, parses itemized invoices, and checks document consistency", "420 ms", "Vision-OCR Engine, Invoice Parser", "Base64 Document Byte Streams (PDF/Images)", "Extracted Table Entities & Invoice Totals", "95%"),
            ("3. Policy Verification Agent", "Retrieves relevant policy clauses from ChromaDB RAG, validates eligibility and waiting periods", "680 ms", "ChromaDB Vector Store, all-MiniLM-L6-v2", "Claim Line, Incident Description, Policy Identifier", "Retrieved Grounded Policy Clauses (Coverage: Covered)", "91%"),
            ("4. Fraud / Risk Analysis Agent", "Evaluates anomaly indicators, loss ratios, and queries MCP Fraud Bureau", "310 ms", "MCP Fraud Bureau API, Anomaly Rules Engine", "Claim ID, Incurred Amount, Provider Geolocation", "Risk Index Score: 0.12 (Low Risk), Zero Flags", "94%"),
            ("5. Claim Assessment Agent", "Synthesizes findings, computes itemized deductible/co-pay payouts, and evaluates HITL need", "550 ms", "Synthesized Multi-Agent Adjudication Engine", "Intake Data, Policy Clauses, OCR Invoices, Risk Profile", "Recommendation: Approved, Net Payable: ₹1,20,000", "90%"),
            ("6. Audit & Compliance Agent", "Generates immutable audit trail, verifies IRDAI regulatory compliance, and stamps token", "120 ms", "SQLite Audit Store, SHA-256 Hasher", "Chronological Audit Events from all Nodes", "Sealed Audit Trace (Token: A7F43E2910BC)", "100%")
        ]

        for name, purpose, latency, tools, in_desc, out_desc, conf in agents:
            agent_html = f"""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px 14px; margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <span style="font-weight:750; color:#0284c7; font-size:13px;">{name}</span>
                    <div style="display:flex; gap:6px;">
                        <span class="status-badge badge-navy">Latency: {latency}</span>
                        <span class="status-badge badge-green">Confidence: {conf}</span>
                    </div>
                </div>
                <div style="font-size:12px; color:#1e293b; line-height:1.4;">{purpose}</div>
                <div style="margin-top:6px; font-size:11px; color:#64748b; display:grid; grid-template-columns: repeat(3, 1fr); gap:8px;">
                    <div><b>Tools:</b> {tools}</div>
                    <div><b>Input:</b> {in_desc}</div>
                    <div><b>Output:</b> {out_desc}</div>
                </div>
            </div>
            """
            render_html(agent_html)
