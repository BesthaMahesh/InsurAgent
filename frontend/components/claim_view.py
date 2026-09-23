"""
Claim Overview and Details component for InsurAgent enterprise UI.
"""
import streamlit as st
import textwrap
from typing import Dict, Any


def render_claim_overview(claim_data: Dict[str, Any]) -> None:
    """Renders the executive Claim Overview grid."""
    claim_id = claim_data.get("claim_id", "N/A")
    claimant = claim_data.get("claimant_name") or claim_data.get("claimant", {}).get("name", "N/A")
    claim_type = claim_data.get("claim_type", "Health")
    policy_id = claim_data.get("policy_number", "N/A")
    amount = float(claim_data.get("amount", 0.0))
    submission_date = claim_data.get("incident_date") or claim_data.get("created_at", "2026-09-18")
    status = claim_data.get("status", "Under Assessment")
    risk_level = claim_data.get("risk_level") or claim_data.get("risk_analysis", {}).get("risk_level", "Low Risk")

    status_badge_class = "badge-green" if "Approv" in status or "Completed" in status else ("badge-amber" if "Review" in status or "Risk" in status else "badge-blue")
    risk_badge_class = "badge-red" if "High" in risk_level or "Investig" in risk_level else ("badge-amber" if "Medium" in risk_level else "badge-green")

    st.markdown(textwrap.dedent(f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:16px; margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #f1f5f9; padding-bottom:10px;">
            <div>
                <div style="font-size:16px; font-weight:800; color:#0f172a;">Claim Record: {claim_id}</div>
                <div style="font-size:12px; color:#64748b;">Enterprise Claim Profile &amp; Adjudication Metadata</div>
            </div>
            <div style="display:flex; gap:8px;">
                <span class="status-badge {status_badge_class}">● {status}</span>
                <span class="status-badge {risk_badge_class}">Risk: {risk_level}</span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; font-size:12.5px;">
            <div><span style="color:#64748b;">Claimant:</span><br><b>{claimant}</b></div>
            <div><span style="color:#64748b;">Policy Number:</span><br><b>{policy_id}</b></div>
            <div><span style="color:#64748b;">Insurance Line:</span><br><b>{claim_type}</b></div>
            <div><span style="color:#64748b;">Claimed Amount:</span><br><b>₹{amount:,.2f}</b></div>
            <div><span style="color:#64748b;">Submission Date:</span><br><b>{submission_date}</b></div>
            <div><span style="color:#64748b;">Recommendation:</span><br><b>{claim_data.get('recommendation', 'Approved')}</b></div>
            <div><span style="color:#64748b;">Confidence:</span><br><b>{float(claim_data.get('confidence', 0.90))*100:.0f}%</b></div>
            <div><span style="color:#64748b;">Review Channel:</span><br><b>Automated Multi-Agent</b></div>
        </div>
        {f'<div style="background:#f8fafc; padding:10px; border-radius:6px; margin-top:12px; font-size:12px;"><b>Incident Description:</b> {claim_data.get("description")}</div>' if claim_data.get('description') else ''}
    </div>
    """), unsafe_allow_html=True)
