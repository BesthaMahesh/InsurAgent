"""
Timeline components for InsurAgent claim processing and audit traces.
"""
import streamlit as st
import textwrap
from typing import List, Dict, Any, Optional


def render_claim_processing_timeline(current_stage_idx: int = 8) -> None:
    """
    Renders the 8-stage enterprise claim processing lifecycle timeline.
    1. Claim Received
    2. Input Validated
    3. Documents Analyzed
    4. Policy Verified
    5. Risk Assessed
    6. Claim Evaluated
    7. Decision Generated
    8. Audit Recorded
    """
    stages = [
        ("1", "Claim Received", "Intake payload captured & parsed", "Claim Intake Agent"),
        ("2", "Input Validated", "PII masked, prompt injection filtered", "Input Guardrail"),
        ("3", "Documents Analyzed", "OCR extraction & invoice verification", "Document Analysis Agent"),
        ("4", "Policy Verified", "Coverage terms & limits retrieved via RAG", "Policy Verification Agent"),
        ("5", "Risk Assessed", "Anomaly indicators evaluated via MCP", "Fraud / Risk Agent"),
        ("6", "Claim Evaluated", "Itemized deduction & payout calculated", "Claim Assessment Agent"),
        ("7", "Decision Generated", "Grounded reasoning & explainability output", "Output Guardrail"),
        ("8", "Audit Recorded", "Immutable audit trail stamped & sealed", "Audit & Compliance Agent")
    ]

    st.markdown(textwrap.dedent("""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:16px; margin-bottom:16px;">
        <div style="font-size:14px; font-weight:750; color:#0f172a; margin-bottom:12px;">Claim Processing Timeline</div>
    </div>
    """), unsafe_allow_html=True)

    cols = st.columns(8)
    for idx, ((num, name, desc, agent), col) in enumerate(zip(stages, cols)):
        is_completed = (idx + 1) <= current_stage_idx
        badge_bg = "#0284c7" if is_completed else "#e2e8f0"
        badge_color = "#ffffff" if is_completed else "#64748b"
        border_color = "#0284c7" if is_completed else "#e2e8f0"

        with col:
            st.markdown(textwrap.dedent(f"""
            <div style="background:#ffffff; border:1px solid {border_color}; border-radius:8px; padding:10px 8px; min-height:105px; display:flex; flex-direction:column; justify-content:space-between;">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="width:20px; height:20px; border-radius:50%; background:{badge_bg}; color:{badge_color}; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:800;">{num}</span>
                        <span style="font-size:9.5px; color:{'#047857' if is_completed else '#64748b'}; font-weight:700;">{'✓ Done' if is_completed else 'Pending'}</span>
                    </div>
                    <div style="font-size:11px; font-weight:700; color:#0f172a; margin-top:6px; line-height:1.2;">{name}</div>
                </div>
                <div style="font-size:9px; color:#64748b; margin-top:4px;">{agent}</div>
            </div>
            """), unsafe_allow_html=True)


def render_audit_trace_timeline(audit_events: List[Dict[str, Any]], trace_id: Optional[str] = None) -> None:
    """Renders the detailed chronological end-to-end audit trace timeline."""
    st.markdown(textwrap.dedent(f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">
            <div style="font-size:14px; font-weight:750; color:#0f172a;">Chronological Audit &amp; Traceability Trail</div>
            <span class="status-badge badge-navy">Trace ID: <code>{trace_id or 'TRC-LIVE-ORCH'}</code></span>
        </div>
    </div>
    """), unsafe_allow_html=True)

    if not audit_events:
        st.info("No audit events recorded for this trace yet.")
        return

    for ev in audit_events:
        t = ev.get("timestamp", "00:00:00")
        agent = ev.get("agent", "System")
        act = ev.get("action", "")
        src = ev.get("source", "")
        status = ev.get("status", "success")
        badge_cls = "badge-green" if status == "success" else "badge-amber"

        st.markdown(textwrap.dedent(f"""
        <div class="timeline-node">
            <div style="font-size:11px; font-weight:700; color:#64748b; width:70px; padding-top:2px;">{t}</div>
            <div class="timeline-content">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; color:#0284c7; font-size:12.5px;">[{agent}]</span>
                    <span class="status-badge {badge_cls}" style="font-size:9.5px;">{status}</span>
                </div>
                <div style="font-size:12px; color:#1e293b; margin-top:2px;">{act}</div>
                {f'<div style="font-size:10px; color:#64748b; margin-top:2px;">Source: <code>{src}</code></div>' if src else ''}
            </div>
        </div>
        """), unsafe_allow_html=True)
