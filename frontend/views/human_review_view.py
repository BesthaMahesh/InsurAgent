"""
Human-in-the-Loop (HITL) Review Workspace for InsurAgent enterprise UI.
"""
import streamlit as st
import pandas as pd
import textwrap
from backend.client import insuragent_client
from frontend.components.timeline import render_audit_trace_timeline


def render_human_review_view() -> None:
    st.markdown('<div class="page-title">Human-in-the-Loop Review Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Manual adjudication and review queue for claims flagged with elevated risk, unverified policy terms, or missing documentation.</div>', unsafe_allow_html=True)

    # Initialize review queue in session_state if not present
    if "hitl_queue" not in st.session_state:
        st.session_state["hitl_queue"] = [
            {"Claim ID": "CLM-20260918-B81C", "Risk Level": "Requires Investigation", "Reason": "Multiple prior claims within 12 months & early policy inception", "AI Recommendation": "Requires Human Review", "Confidence": "65%", "Assigned Reviewer": "Senior Adjuster (Mahesh S.)", "Status": "Pending Review"},
            {"Claim ID": "CLM-20260918-C42D", "Risk Level": "Medium Risk", "Reason": "Missing original discharge summary and high claimed amount (₹2.1L)", "AI Recommendation": "Requires Human Review", "Confidence": "70%", "Assigned Reviewer": "Senior Adjuster (Mahesh S.)", "Status": "Pending Review"},
            {"Claim ID": "CLM-20260920-E91X", "Risk Level": "Medium Risk", "Reason": "Specialty cyber loss sub-limit ceiling verification required", "AI Recommendation": "Requires Human Review", "Confidence": "72%", "Assigned Reviewer": "Specialty Underwriter", "Status": "Pending Review"}
        ]

    st.markdown("##### 📋 Claims Flagged for Manual Adjuster Review")
    st.dataframe(pd.DataFrame(st.session_state["hitl_queue"]), use_container_width=True, hide_index=True)

    st.write("")

    # ---------- Selected Claim Adjudication Workspace ----------
    with st.container(border=True):
        st.markdown("##### 🔍 Selected Claim Investigation: `CLM-20260918-B81C`")
        
        c1, c2 = st.columns([1.5, 1])

        with c1:
            st.markdown(textwrap.dedent("""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px; margin-bottom:12px; font-size:12.5px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <b>Claimant:</b> Priya Patel | <b>Policy:</b> POL-MOTOR-COMP-2026 | <b>Line:</b> Motor
                    <span class="status-badge badge-amber">Status: Review Required</span>
                </div>
                <div><b>Incurred Amount:</b> ₹82,500.00 | <b>Incident Date:</b> 2026-09-15</div>
                <div style="margin-top:4px;"><b>Description:</b> Front bumper and radiator collision damage repair estimate submitted from Apex Auto Workshop.</div>
            </div>
            """), unsafe_allow_html=True)

            st.markdown("###### 🤖 AI Recommendation & Decision Context")
            st.markdown("""
            - **Recommendation**: `Requires Human Review (Adjudication Checkpoint)`
            - **Confidence Index**: `0.65 / 1.00`
            - **Reasoning**: Claim filed within 14 days of policy inception. Workshop flagged for estimate discrepancies.
            - **Deductible Applicable**: `₹1,000 Standard Compulsory Deductible`
            """)

            st.markdown("###### 🚨 Risk Indicators (MCP Fraud Bureau)")
            st.markdown("""
            1. Claim filed within 14 days of policy inception.
            2. Multiple prior claims recorded across different insurers in past 12 months.
            3. Workshop flagged for estimate discrepancies.
            """)

        with c2:
            st.markdown("###### ⚖️ Adjuster Decision Actions")
            st.info("Review all supporting evidence and policy clauses before selecting an adjudication decision.")

            note = st.text_area("Adjuster Review Note & Compliance Justification", height=90, placeholder="Enter reason for approval, rejection or additional investigation...")

            b1, b2 = st.columns(2)
            with b1:
                if st.button("✓ Approve Claim", type="primary", use_container_width=True):
                    st.success("Claim CLM-20260918-B81C approved by Senior Adjuster. Straight-through payment queued.")
                    st.session_state["hitl_queue"][0]["Status"] = "Approved by Adjuster"
            with b2:
                if st.button("✗ Reject Claim", use_container_width=True):
                    st.warning("Claim CLM-20260918-B81C rejected. Formal rejection letter with IRDAI grievance clause generated.")
                    st.session_state["hitl_queue"][0]["Status"] = "Rejected"

            b3, b4 = st.columns(2)
            with b3:
                if st.button("📄 Request Info", use_container_width=True):
                    st.info("Information request dispatched to claimant for original repair invoices.")
                    st.session_state["hitl_queue"][0]["Status"] = "Awaiting Info"
            with b4:
                if st.button("⚠️ Escalate to SIU", use_container_width=True):
                    st.error("Escalated to Special Investigation Unit (SIU) for on-site workshop survey.")
                    st.session_state["hitl_queue"][0]["Status"] = "SIU Escalation"

    # Audit Trail for this flagged claim
    events = insuragent_client.get_audit_trail("CLM-20260918-B81C")
    if not events:
        events = [
            {"timestamp": "09:30:01", "agent": "InputGuardrail", "action": "Input validation passed (PII Redacted).", "source": "Deterministic Guardrails", "status": "success"},
            {"timestamp": "09:30:04", "agent": "RiskAgent", "action": "Risk Score evaluated at 0.68 (Requires Investigation).", "source": "MCP Fraud Bureau", "status": "flagged"},
            {"timestamp": "09:30:06", "agent": "HumanReviewNode", "action": "Mandatory human review checkpoint triggered.", "source": "HITL Orchestrator", "status": "review_required"}
        ]
    render_audit_trace_timeline(events, trace_id="TRC-HITL-B81C")
