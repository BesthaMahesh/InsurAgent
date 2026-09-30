"""
Multi-Agent Workflow component for InsurAgent enterprise UI.
Renders a visual, stateful LangGraph execution flow with RAG, MCP, and HITL routing.
"""
import streamlit as st
from typing import Dict, Any, Optional
from frontend.styles import render_html


def render_workflow_diagram(active_state: Optional[Dict[str, Any]] = None) -> None:
    """
    Renders the visual multi-agent orchestration architecture flow.
    Reflects live LangGraph execution state, RAG & MCP connections, and HITL branching.
    """
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
        h_col1, h_col2 = st.columns([3, 1.2])
        with h_col1:
            render_html("""
            <div style="font-size:14.5px; font-weight:800; color:#0f172a; margin-bottom:2px;">
                Claim Processing Flow &amp; Agent Execution
            </div>
            <div style="font-size:11.5px; color:#64748b;">
                Autonomous multi-agent pipeline with deterministic guardrails, RAG vector retrieval, and MCP tools.
            </div>
            """)
        with h_col2:
            render_html(f"""
            <div style="text-align:right;">
                <span class="status-badge {'badge-amber' if req_human else 'badge-green'}">
                    {'● Route: Human-in-the-Loop Review' if req_human else '● Route: Straight-Through Adjudication'}
                </span>
            </div>
            """)

        st.write("")

        # 7-Step Responsive Flow Grid
        flow_steps = [
            ("SUPERVISOR", "Supervisor", "Goal Decomposed", "badge-navy", "7 Subtasks Planned"),
            ("AGENT 1", "Claim Intake", "Intake Normalized", "badge-green", "100% Complete"),
            ("AGENT 2", "Document Intel", "OCR Extracted", "badge-green", "Invoices Verified"),
            ("AGENT 3", "Policy Verify", "RAG Retrieved", "badge-purple", f"{'Covered' if has_evidence else 'Review'} (ChromaDB)"),
            ("AGENT 4", "Fraud / Risk", "MCP Evaluated", "badge-amber" if risk_res.get("risk_score", 0.12) > 0.40 else "badge-green", f"Score: {risk_res.get('risk_score', 0.12):.2f}"),
            ("AGENT 5", "Assessment", "Payout Calculated", "badge-blue", rec[:18] + "..."),
            ("AGENT 6", "Audit & Legal", "Audit Sealed", "badge-green", "IRDAI Stamped")
        ]

        # Use responsive CSS grid instead of 7 tight columns to prevent horizontal overflow
        grid_items_html = ""
        for step_num, title, action, badge_style, subtext in flow_steps:
            grid_items_html += f"""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:10px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 1px 3px rgba(0,0,0,0.02); min-height:110px;">
                <div>
                    <div style="font-size:9.5px; font-weight:800; color:#0284c7;">{step_num}</div>
                    <div style="font-size:12px; font-weight:750; color:#0f172a; margin-top:2px; line-height:1.2;">{title}</div>
                </div>
                <div>
                    <span class="status-badge {badge_style}" style="font-size:9.5px; padding:2px 6px; margin:4px 0;">{action}</span>
                    <div style="font-size:9.5px; color:#64748b;">{subtext}</div>
                </div>
            </div>
            """

        render_html(f"""
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:10px; margin-bottom:12px;">
            {grid_items_html}
        </div>
        """)

        # Routing and Connected Systems Sub-Panel
        r1, r2, r3 = st.columns([1.2, 1.2, 1.5])
        with r1:
            render_html("""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:8px 10px; font-size:11px;">
                <b style="color:#7e22ce;">📚 Knowledge Layer (RAG):</b><br>
                <span>ChromaDB Vector Store • 41 Chunks • Zero-Hallucination Grounding</span>
            </div>
            """)
        with r2:
            render_html("""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:8px 10px; font-size:11px;">
                <b style="color:#0369a1;">🔌 Integration Layer (MCP):</b><br>
                <span>4 Core Systems: PAS, Claims DB, CRM, Fraud Bureau</span>
            </div>
            """)
        with r3:
            routing_desc = f"⚠️ Escalated: {human_reason}" if (req_human and human_reason) else ("⚠️ Escalated to Senior Adjuster" if req_human else "✓ Straight-Through Approval to Settlement")
            render_html(f"""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:8px 10px; font-size:11px;">
                <b style="color:{'#b45309' if req_human else '#047857'};">⚖️ Adjudication Routing Path:</b><br>
                <span>{routing_desc}</span>
            </div>
            """)
