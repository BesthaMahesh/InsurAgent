"""
Timeline components for InsurAgent claim processing and audit traces.
"""
import streamlit as st
from typing import List, Dict, Any, Optional
from frontend.styles import render_html


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
        ("1", "Claim Received", "Intake captured", "Claim Intake Agent"),
        ("2", "Input Validated", "PII masked & safe", "Input Guardrail"),
        ("3", "Documents Analyzed", "OCR extraction", "Document Analysis Agent"),
        ("4", "Policy Verified", "Coverage terms", "Policy Verification Agent"),
        ("5", "Risk Assessed", "Anomaly check", "Fraud / Risk Agent"),
        ("6", "Claim Evaluated", "Payout calculated", "Claim Assessment Agent"),
        ("7", "Decision Generated", "Explainability output", "Output Guardrail"),
        ("8", "Audit Recorded", "Immutable seal", "Audit & Compliance Agent")
    ]

    items_html = ""
    for idx, (num, name, desc, agent) in enumerate(stages):
        is_completed = (idx + 1) <= current_stage_idx
        badge_bg = "#0284c7" if is_completed else "#e2e8f0"
        badge_color = "#ffffff" if is_completed else "#64748b"
        border_color = "#0284c7" if is_completed else "#e2e8f0"
        status_text = "✓ Completed" if is_completed else "Pending"
        status_color = "#047857" if is_completed else "#64748b"

        items_html += f"""
        <div style="background:#ffffff; border:1px solid {border_color}; border-radius:8px; padding:10px 8px; min-height:95px; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="width:20px; height:20px; border-radius:50%; background:{badge_bg}; color:{badge_color}; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:800;">{num}</span>
                    <span style="font-size:9.5px; color:{status_color}; font-weight:700;">{status_text}</span>
                </div>
                <div style="font-size:11px; font-weight:700; color:#0f172a; margin-top:6px; line-height:1.2;">{name}</div>
            </div>
            <div style="font-size:9px; color:#64748b; margin-top:4px;">{agent}</div>
        </div>
        """

    render_html(f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:16px; margin-bottom:16px;">
        <div style="font-size:14px; font-weight:750; color:#0f172a; margin-bottom:12px;">Claim Processing Timeline</div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(115px, 1fr)); gap:8px;">
            {items_html}
        </div>
    </div>
    """)


def render_audit_trace_timeline(audit_events: List[Dict[str, Any]], trace_id: Optional[str] = None) -> None:
    """Renders the detailed chronological end-to-end audit trace timeline."""
    render_html(f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:16px; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">
            <div style="font-size:14px; font-weight:750; color:#0f172a;">Chronological Audit &amp; Traceability Trail</div>
            <span class="status-badge badge-navy">Trace ID: <code>{trace_id or 'TRC-LIVE-ORCH'}</code></span>
        </div>
    </div>
    """)

    if not audit_events:
        st.info("No audit events recorded for this trace yet.")
        return

    nodes_html = ""
    for ev in audit_events:
        t = ev.get("timestamp", "00:00:00")
        agent = ev.get("agent", "System")
        act = ev.get("action", "")
        src = ev.get("source", "")
        status = ev.get("status", "success")
        badge_cls = "badge-green" if status == "success" else "badge-amber"
        src_html = f'<div style="font-size:10px; color:#64748b; margin-top:2px;">Source: <code>{src}</code></div>' if src else ''

        nodes_html += f"""
        <div class="timeline-node">
            <div style="font-size:11px; font-weight:700; color:#64748b; width:70px; padding-top:2px;">{t}</div>
            <div class="timeline-content">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; color:#0284c7; font-size:12.5px;">[{agent}]</span>
                    <span class="status-badge {badge_cls}" style="font-size:9.5px;">{status}</span>
                </div>
                <div style="font-size:12px; color:#1e293b; margin-top:2px;">{act}</div>
                {src_html}
            </div>
        </div>
        """

    render_html(nodes_html)
