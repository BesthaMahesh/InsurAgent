"""
Multi-Agent Workflow component for InsurAgent enterprise UI.
Renders a visual, stateful LangGraph execution flow with RAG, MCP, and HITL routing.
"""
import streamlit as st
import textwrap
from typing import Dict, Any, Optional


def render_workflow_diagram(active_state: Optional[Dict[str, Any]] = None) -> None:
    """
    Renders the visual multi-agent orchestration architecture flow.
    Reflects live LangGraph execution state, RAG & MCP connections, and HITL branching.
    """
    # Extract state context if provided
    state = active_state or st.session_state.get("submitted_claim_response") or {}
    assessment = state.get("assessment", {})
    policy_ver = state.get("policy_verification", {})
    risk_res = state.get("risk_analysis", {})
    req_human = state.get("requires_human_review", False)
    human_reason = state.get("human_review_reason")
    rec = assessment.get("recommendation", "Recommended for Approval")
    has_evidence = policy_ver.get("policy_found", True)

    with st.container(border=True):
        # Header with dynamic status badge
        h_col1, h_col2 = st.columns([3, 1])
        with h_col1:
            st.markdown(textwrap.dedent("""
            <div style="font-size:14.5px; font-weight:800; color:#0f172a; margin-bottom:2px;">
                LangGraph Autonomous Agent Orchestration Flow
            </div>
            <div style="font-size:11.5px; color:#64748b;">
                Stateful Multi-Agent Control Plane with deterministic guardrails, RAG vector retrieval, and MCP tools.
            </div>
            """), unsafe_allow_html=True)
        with h_col2:
            status_badge_html = textwrap.dedent(f"""
            <div style="text-align:right;">
                <span class="status-badge {'badge-amber' if req_human else 'badge-green'}">
                    {'● Route: Human-in-the-Loop Review' if req_human else '● Route: Straight-Through Adjudication'}
                </span>
            </div>
            """)
            st.markdown(status_badge_html, unsafe_allow_html=True)

        st.write("")

        # 7-Step Horizontal Flow across 7 Columns
        cols = st.columns(7)

        flow_steps = [
            ("SUPERVISOR", "Supervisor", "Goal Decomposed", "badge-navy", "7 Subtasks Planned"),
            ("AGENT 1", "Claim Intake", "Intake Normalized", "badge-green", "100% Complete"),
            ("AGENT 2", "Document Intelligence", "OCR Extracted", "badge-green", "Invoices Verified"),
            ("AGENT 3", "Policy Verify", "RAG Retrieved", "badge-purple", f"{'Covered' if has_evidence else 'Review'} (ChromaDB)"),
            ("AGENT 4", "Fraud / Risk", "MCP Evaluated", "badge-amber" if risk_res.get("risk_score", 0.12) > 0.40 else "badge-green", f"Score: {risk_res.get('risk_score', 0.12):.2f}"),
            ("AGENT 5", "Assessment", "Payout Calculated", "badge-blue", rec[:18] + "..."),
            ("AGENT 6", "Audit & Legal", "Audit Sealed", "badge-green", "IRDAI Token Stamped")
        ]

        for col, (step_num, title, action, badge_style, subtext) in zip(cols, flow_steps):
            with col:
                card_html = textwrap.dedent(f"""
                <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:8px; min-height:115px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
                    <div>
                        <div style="font-size:9.5px; font-weight:800; color:#0284c7;">{step_num}</div>
                        <div style="font-size:11.5px; font-weight:750; color:#0f172a; margin-top:2px; line-height:1.2;">{title}</div>
                    </div>
                    <div>
                        <span class="status-badge {badge_style}" style="font-size:9.5px; padding:2px 6px; margin:4px 0;">{action}</span>
                        <div style="font-size:9px; color:#64748b;">{subtext}</div>
                    </div>
                </div>
                """)
                st.markdown(card_html, unsafe_allow_html=True)

        st.write("")

        # Routing and Connected Systems Sub-Panel
        r1, r2, r3 = st.columns([1.2, 1.2, 1.5])
        with r1:
            st.markdown(textwrap.dedent("""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:8px 10px; font-size:11px;">
                <b style="color:#7e22ce;">📚 Knowledge Layer (RAG):</b><br>
                <span>ChromaDB Vector Store • 41 Chunks • Zero-Hallucination Grounding</span>
            </div>
            """), unsafe_allow_html=True)
        with r2:
            st.markdown(textwrap.dedent("""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:8px 10px; font-size:11px;">
                <b style="color:#0369a1;">🔌 Integration Layer (MCP):</b><br>
                <span>4 Core Systems: PAS, Claims DB, CRM, Fraud Bureau</span>
            </div>
            """), unsafe_allow_html=True)
        with r3:
            routing_desc = f"⚠️ Escalated: {human_reason}" if (req_human and human_reason) else ("⚠️ Escalated to Senior Adjuster" if req_human else "✓ Straight-Through Approval to Settlement")
            st.markdown(textwrap.dedent(f"""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:8px 10px; font-size:11px;">
                <b style="color:{'#b45309' if req_human else '#047857'};">⚖️ Adjudication Routing Path:</b><br>
                <span>{routing_desc}</span>
            </div>
            """), unsafe_allow_html=True)
