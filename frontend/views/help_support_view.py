"""
Help & Support View for InsurAgent End User Experience.
Provides policyholders and adjusters with FAQs, claims filing guides,
support channels, and regulatory grievance escalation procedures.
"""
import streamlit as st
from frontend.styles import render_html


def render_help_support_view() -> None:
    """Renders the Help & Support center for business users."""
    render_html('<div class="page-title">Help &amp; Support</div>')
    render_html('<div class="page-subtitle">Assistance with claim filing, policy questions, escalation procedures, and support channels.</div>')

    # ---------- Top Support Cards ----------
    c1, c2, c3 = st.columns(3)
    with c1:
        render_html("""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:16px; min-height:140px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span style="font-size:20px;">📞</span>
                <span style="font-weight:750; font-size:14px; color:#0f172a;">24/7 Claims Helpline</span>
            </div>
            <div style="font-size:12px; color:#64748b; line-height:1.5;">Toll-Free assistance for emergency claims intake and hospitalization authorization.</div>
            <div style="font-size:13px; font-weight:750; color:#0284c7; margin-top:8px;">1800-419-7890 (Toll-Free)</div>
        </div>
        """)
    with c2:
        render_html("""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:16px; min-height:140px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span style="font-size:20px;">✉️</span>
                <span style="font-weight:750; font-size:14px; color:#0f172a;">Claims Support Desk</span>
            </div>
            <div style="font-size:12px; color:#64748b; line-height:1.5;">Direct email support for document submission and adjudication status inquiries.</div>
            <div style="font-size:13px; font-weight:750; color:#0284c7; margin-top:8px;">claims.support@insuragent.com</div>
        </div>
        """)
    with c3:
        render_html("""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:16px; min-height:140px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span style="font-size:20px;">💬</span>
                <span style="font-weight:750; font-size:14px; color:#0f172a;">AI Policy Assistant</span>
            </div>
            <div style="font-size:12px; color:#64748b; line-height:1.5;">Instant 24/7 answers regarding policy coverage, waiting periods, and deductible terms.</div>
            <div style="font-size:13px; font-weight:750; color:#0284c7; margin-top:8px;">Available in Navigation Menu</div>
        </div>
        """)

    st.write("")

    # ---------- Frequently Asked Questions (FAQ) ----------
    with st.container(border=True):
        st.markdown("##### ❓ Frequently Asked Questions (FAQs)")
        
        with st.expander("Q: How do I submit an insurance claim?"):
            st.write("Navigate to **Claims** in the sidebar, select the **Submit New Claim** tab, fill out claimant and incident particulars, attach at least one mandatory supporting document (Hospital Bill, Invoice, or Estimate), and click Submit.")

        with st.expander("Q: Why are supporting documents mandatory?"):
            st.write("Supporting documents are required by insurance underwriting standards to verify incident expenses, eliminate fraud, validate hospital/workshop diagnoses, and ensure accurate deductible computation.")

        with st.expander("Q: What is the waiting period for pre-existing diseases (PED)?"):
            st.write("Under the Standard Gold Health Policy, pre-existing diseases are subject to a 24-month continuous coverage waiting period before inpatient hospitalization expenses become eligible for claim settlement.")

        with st.expander("Q: How long does claim adjudication take?"):
            st.write("Standard straight-through claims are processed and adjudicated in under 1 second. Claims flagged for human investigation or requiring additional invoices are typically reviewed within 24 to 48 business hours.")

        with st.expander("Q: What should I do if my claim requires human review?"):
            st.write("If your claim is flagged for human review, our senior claims adjudicator will review the uploaded documents. If additional information is needed, an email notification will be dispatched to the claimant.")

    st.write("")

    # ---------- Grievance & Regulatory Escalation ----------
    with st.container(border=True):
        st.markdown("##### ⚖️ Grievance Redressal & IRDAI Regulatory Standards")
        render_html("""
        <div style="font-size:12.5px; line-height:1.6; color:#334155;">
            InsurAgent adheres strictly to <b>IRDAI Health &amp; General Insurance Adjudication Regulations 2026</b>.<br>
            If you have an unresolved dispute regarding claim settlement amounts or deductions:
            <ul style="margin-top:6px; padding-left:18px;">
                <li><b>Level 1:</b> Contact your dedicated Senior Claims Officer at <code>grievance@insuragent.com</code>.</li>
                <li><b>Level 2:</b> Escalate to the Principal Grievance Officer (PGO) with your Claim ID and Reproducibility Token.</li>
                <li><b>Level 3:</b> If unresolved after 30 days, register a complaint with the Insurance Ombudsman (IRDAI Bima Bharosa Portal).</li>
            </ul>
        </div>
        """)
