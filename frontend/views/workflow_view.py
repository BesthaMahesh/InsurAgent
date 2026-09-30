"""
Agent Workflow View for InsurAgent Developer Experience.
Presents the technical multi-agent LangGraph orchestrator, state schema (AgentState),
conditional routing rules, and node-level input/output specifications.
"""
import streamlit as st
import pandas as pd
from frontend.styles import render_html


def render_workflow_view() -> None:
    """Renders the developer Agent Workflow architecture and LangGraph state view."""
    render_html('<div class="page-title">Agent Workflow</div>')
    render_html('<div class="page-subtitle">Monitor AI agents, workflow execution, conditional routing, LangGraph state machine, and node-level contracts.</div>')

    # ---------- 1. Technical Execution DAG Banner ----------
    with st.container(border=True):
        st.markdown("##### ⚙️ Multi-Agent LangGraph Execution Pipeline (DAG)")
        render_html("""
        <div style="background:#091524; border:1px solid #1e2e42; border-radius:10px; padding:16px; margin-bottom:10px; color:#ffffff;">
            <div style="font-size:11px; font-weight:800; color:#38bdf8; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:10px;">Deterministic End-to-End Orchestration Flow</div>
            <div style="display:flex; flex-wrap:wrap; align-items:center; gap:8px; font-size:11px;">
                <span style="background:#1e3a5f; padding:5px 8px; border-radius:6px; color:#ffffff;">User Request</span> →
                <span style="background:#0284c7; padding:5px 8px; border-radius:6px; color:#ffffff; font-weight:700;">Input Guardrail</span> →
                <span style="background:#1e3a5f; padding:5px 8px; border-radius:6px; color:#ffffff;">Supervisor Agent</span> →
                <span style="background:#1e3a5f; padding:5px 8px; border-radius:6px; color:#ffffff;">Claim Intake Agent</span> →
                <span style="background:#1e3a5f; padding:5px 8px; border-radius:6px; color:#ffffff;">Document Analysis</span> →
                <span style="background:#0284c7; padding:5px 8px; border-radius:6px; color:#ffffff; font-weight:700;">Policy Verification (RAG)</span> →
                <span style="background:#1e3a5f; padding:5px 8px; border-radius:6px; color:#ffffff;">Risk &amp; Fraud (MCP)</span> →
                <span style="background:#1e3a5f; padding:5px 8px; border-radius:6px; color:#ffffff;">Claim Assessment</span> →
                <span style="background:#d97706; padding:5px 8px; border-radius:6px; color:#ffffff; font-weight:700;">HITL Router</span> →
                <span style="background:#1e3a5f; padding:5px 8px; border-radius:6px; color:#ffffff;">Audit &amp; Compliance</span> →
                <span style="background:#047857; padding:5px 8px; border-radius:6px; color:#ffffff; font-weight:700;">Output Guardrail</span> →
                <span style="background:#047857; padding:5px 8px; border-radius:6px; color:#ffffff; font-weight:700;">Final Response</span>
            </div>
        </div>
        """)

    st.write("")

    # ---------- 2. Conditional Routing & Decision Logic ----------
    with st.container(border=True):
        st.markdown("##### 🔀 Conditional Routing Logic & Thresholds")
        render_html("""
        <div style="font-size:12.5px; line-height:1.6; color:#334155; margin-bottom:10px;">
            The LangGraph state machine uses deterministic branch points between <b>Claim Assessment</b>, <b>HITL Router</b>, and <b>Audit Agent</b>:
        </div>
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; font-size:12px;">
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px;">
                <div style="font-weight:750; color:#dc2626; margin-bottom:4px;">🚨 Risk Threshold Trigger</div>
                <div><b>Condition:</b> <code>risk_score &ge; 0.60</code></div>
                <div style="color:#64748b; margin-top:2px;">Routes to <b>Human Review Queue</b> for adjuster investigation.</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px;">
                <div style="font-weight:750; color:#d97706; margin-bottom:4px;">🎯 Confidence Floor Trigger</div>
                <div><b>Condition:</b> <code>confidence &lt; 0.85</code></div>
                <div style="color:#64748b; margin-top:2px;">Escalates to senior adjuster when policy evidence is ambiguous.</div>
            </div>
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px;">
                <div style="font-weight:750; color:#047857; margin-bottom:4px;">⚡ Straight-Through Route</div>
                <div><b>Condition:</b> <code>risk &lt; 0.60 AND conf &ge; 0.85</code></div>
                <div style="color:#64748b; margin-top:2px;">Immediate settlement approval and cryptographic audit seal.</div>
            </div>
        </div>
        """)

    st.write("")

    # ---------- 3. Specialized Agent Specifications Registry ----------
    with st.container(border=True):
        st.markdown("##### 🤖 Specialized Agent Specifications")
        
        agents = [
            ("Supervisor / Orchestrator Agent", "Goal Understanding, Task Decomposition, Tool Routing & Memory Context Management", "145 ms", "LangGraph State Engine, Memory Manager", "Raw Claim Payload / Query", "Decomposed Execution Plan (7 Subtasks)", "100%"),
            ("1. Claim Intake Agent", "Classifies line of business, normalizes entity fields, and validates record completeness", "180 ms", "Intake Validation Rules, Entity Normalizer", "Claimant Profile, Policy No, Incident Particulars", "Normalized Claim JSON (100% Completeness)", "98%"),
            ("2. Document Analysis Agent", "Performs computer vision OCR, parses itemized invoices, and checks document consistency", "420 ms", "Vision-OCR Engine, Invoice Parser", "Base64 Document Byte Streams (PDF/Images)", "Extracted Table Entities & Invoice Totals", "95%"),
            ("3. Policy Verification Agent", "Retrieves relevant policy clauses from ChromaDB RAG, validates eligibility and waiting periods", "680 ms", "ChromaDB Vector Store, all-MiniLM-L6-v2", "Claim Line, Incident Description, Policy No", "Retrieved Grounded Policy Clauses (Covered)", "91%"),
            ("4. Fraud / Risk Analysis Agent", "Evaluates anomaly indicators, loss ratios, and queries MCP Fraud Bureau", "310 ms", "MCP Fraud Bureau API, Anomaly Rules Engine", "Claim ID, Incurred Amount, Provider Geolocation", "Risk Score: 0.12 (Low Risk), Zero Flags", "94%"),
            ("5. Claim Assessment Agent", "Synthesizes findings, computes itemized deductible/co-pay payouts, and evaluates HITL need", "550 ms", "Synthesized Multi-Agent Adjudication Engine", "Intake Data, Policy Clauses, OCR Invoices, Risk", "Recommendation: Approved, Net: ₹1,20,000", "90%"),
            ("6. Audit & Compliance Agent", "Generates immutable audit trail, verifies IRDAI regulatory compliance, and stamps token", "120 ms", "SQLite Audit Store, SHA-256 Hasher", "Chronological Audit Events from All Nodes", "Sealed Audit Trace (Token: A7F43E2910BC)", "100%")
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

    st.write("")

    # ---------- 4. LangGraph AgentState TypedDict Schema ----------
    with st.container(border=True):
        st.markdown("##### 📦 LangGraph `AgentState` Typed Schema")
        state_fields = [
            {"Field": "claim_id", "Type": "str", "Description": "Unique enterprise claim identifier (e.g. CLM-20260918-A12F)"},
            {"Field": "trace_id", "Type": "str", "Description": "Distributed tracing ID for cross-agent execution telemetry"},
            {"Field": "claimant", "Type": "Dict[str, Any]", "Description": "Normalized claimant profile (name, email, phone)"},
            {"Field": "claim_details", "Type": "Dict[str, Any]", "Description": "Policy number, claim type, amount, incident date, description"},
            {"Field": "documents", "Type": "List[Dict[str, Any]]", "Description": "Base64 encoded supporting documents and metadata"},
            {"Field": "extracted_document_data", "Type": "Dict[str, Any]", "Description": "Vision-OCR extracted table rows and invoice amounts"},
            {"Field": "policy_context", "Type": "List[Dict[str, Any]]", "Description": "Top-K grounded policy clauses retrieved from ChromaDB"},
            {"Field": "risk_analysis", "Type": "Dict[str, Any]", "Description": "Risk level, numerical score (0-1), MCP bureau flags"},
            {"Field": "assessment", "Type": "Dict[str, Any]", "Description": "Recommendation, itemized gross/copay/deductible/net payout"},
            {"Field": "requires_human_review", "Type": "bool", "Description": "Deterministic boolean flag triggering HITL queue"},
            {"Field": "audit_events", "Type": "List[Dict[str, Any]]", "Description": "Chronological execution audit trail and SHA-256 state hashes"}
        ]
        st.dataframe(pd.DataFrame(state_fields), use_container_width=True, hide_index=True)

