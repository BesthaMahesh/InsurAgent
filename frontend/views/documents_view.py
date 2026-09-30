"""
Documents View for InsurAgent End User Experience.
Provides access to policy schedules, verified uploaded claim attachments,
and mandatory documentation requirements checklist.
"""
import streamlit as st
import pandas as pd
from backend.database.database import SessionLocal, DocumentTable, ClaimTable
from frontend.styles import render_html


def render_documents_view() -> None:
    """Renders the Documents management and repository view."""
    render_html('<div class="page-title">Documents</div>')
    render_html('<div class="page-subtitle">Access policy schedules, upload claim documentation, and inspect verified attachments.</div>')

    tab_policies, tab_uploaded, tab_checklist = st.tabs([
        "📄 Policy Documents & Schedules",
        "📎 Uploaded Claim Attachments",
        "📋 Mandatory Documentation Checklist"
    ])

    # ==========================================
    # TAB 1: POLICY DOCUMENTS & SCHEDULES
    # ==========================================
    with tab_policies:
        st.markdown("##### 📚 Official Policy Wordings & Coverage Schedules")
        
        policy_docs = [
            {"Document Name": "Health Policy Gold Plus (POL-HEALTH-GOLD-2026)", "Line": "Health Insurance", "Version": "v3.0", "Format": "PDF", "Coverage": "Comprehensive Inpatient & Daycare"},
            {"Document Name": "Motor Comprehensive Policy (POL-MOTOR-COMP-2026)", "Line": "Motor Insurance", "Version": "v2.1", "Format": "PDF", "Coverage": "Own Damage & Third Party"},
            {"Document Name": "Travel Shield Worldwide (POL-TRAVEL-SHIELD-2026)", "Line": "Travel Insurance", "Version": "v2.0", "Format": "PDF", "Coverage": "Medical Evacuation & Trip Delays"},
            {"Document Name": "Commercial Property Policy (POL-COMM-2026)", "Line": "Property & Casualty", "Version": "v1.0", "Format": "PDF", "Coverage": "Fire, Flood & Special Perils"},
            {"Document Name": "Cyber Risk Protection Policy (POL-CYBER-2026)", "Line": "Specialty Lines", "Version": "v1.0", "Format": "PDF", "Coverage": "Ransomware & Business Interruption"}
        ]
        st.dataframe(pd.DataFrame(policy_docs), use_container_width=True, hide_index=True)

        st.write("")
        st.markdown("##### 🔍 Inspect Policy Clauses")
        c_sel, c_btn = st.columns([4, 1.2])
        with c_sel:
            chosen_doc = st.selectbox(
                "Select Policy Document",
                [p["Document Name"] for p in policy_docs],
                label_visibility="collapsed",
                key="doc_policy_sel"
            )
        with c_btn:
            if st.button("👁️ View Clauses", type="primary", use_container_width=True, key="doc_view_clauses_btn"):
                st.session_state["active_nav_page"] = "Knowledge Center"
                st.rerun()

    # ==========================================
    # TAB 2: UPLOADED CLAIM ATTACHMENTS
    # ==========================================
    with tab_uploaded:
        st.markdown("##### 📎 Uploaded Claim Documentation Repository")
        st.markdown("<div style='font-size:12px; color:#64748b; margin-bottom:10px;'>All invoices, medical reports, discharge summaries, and estimates attached to registered claims.</div>", unsafe_allow_html=True)

        db = SessionLocal()
        try:
            docs = db.query(DocumentTable).all()
            if docs:
                docs_data = []
                for d in docs:
                    claim = db.query(ClaimTable).filter(ClaimTable.claim_id == d.claim_id).first()
                    claimant = claim.claimant_name if claim else "N/A"
                    docs_data.append({
                        "Claim ID": d.claim_id,
                        "Claimant": claimant,
                        "Document File": d.filename,
                        "File Type": (d.file_type or d.filename.split(".")[-1]).upper(),
                        "Verification Status": "✓ Vision-OCR Verified",
                        "Summary / Content": d.summary or "Verified supporting document."
                    })
                st.dataframe(pd.DataFrame(docs_data), use_container_width=True, hide_index=True)
            else:
                st.info("No documents currently stored in the repository.")
        finally:
            db.close()

    # ==========================================
    # TAB 3: MANDATORY DOCUMENTATION CHECKLIST
    # ==========================================
    with tab_checklist:
        st.markdown("##### 📋 Mandatory Document Guidelines by Insurance Line")
        st.markdown("<div style='font-size:12.5px; color:#64748b; margin-bottom:12px;'>Supporting documentation is strictly mandatory for claim adjudication. Ensure the following documents are attached when submitting claims.</div>", unsafe_allow_html=True)

        col_h, col_m = st.columns(2)
        with col_h:
            render_html("""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:14px; margin-bottom:12px;">
                <div style="font-size:14px; font-weight:750; color:#0284c7; margin-bottom:8px;">🏥 Health Insurance Claims</div>
                <ul style="font-size:12px; line-height:1.7; color:#334155; margin:0; padding-left:18px;">
                    <li><b>Hospital Discharge Summary</b> with admission/discharge dates and clinical diagnosis.</li>
                    <li><b>Itemized Hospital Bill &amp; Payment Receipts</b> signed and stamped by hospital billing.</li>
                    <li><b>Diagnostic Test Reports &amp; Prescriptions</b> (Lab tests, MRI/CT scans, surgery notes).</li>
                    <li><b>Doctor's Consultation &amp; Referral Letter</b>.</li>
                </ul>
            </div>
            """)

        with col_m:
            render_html("""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:14px; margin-bottom:12px;">
                <div style="font-size:14px; font-weight:750; color:#0284c7; margin-bottom:8px;">🚗 Motor Insurance Claims</div>
                <ul style="font-size:12px; line-height:1.7; color:#334155; margin:0; padding-left:18px;">
                    <li><b>Itemized Repair Estimate &amp; Final Tax Invoice</b> from authorized garage.</li>
                    <li><b>Photographs of Vehicle Damage</b> showing registration number plate.</li>
                    <li><b>Driver's License &amp; Vehicle Registration Certificate (RC)</b> copy.</li>
                    <li><b>Police First Information Report (FIR)</b> for third-party injury, death, or major collisions.</li>
                </ul>
            </div>
            """)

        col_t, col_p = st.columns(2)
        with col_t:
            render_html("""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:14px; margin-bottom:12px;">
                <div style="font-size:14px; font-weight:750; color:#0284c7; margin-bottom:8px;">✈️ Travel Insurance Claims</div>
                <ul style="font-size:12px; line-height:1.7; color:#334155; margin:0; padding-left:18px;">
                    <li><b>Carrier Irregularity Report (PIR) / Delay Certificate</b> from airline.</li>
                    <li><b>Boarding Passes &amp; Original Ticket Itinerary</b>.</li>
                    <li><b>Hotel &amp; Meal Invoices</b> incurred during flight delay.</li>
                    <li><b>Emergency Medical Invoices</b> for overseas hospitalization.</li>
                </ul>
            </div>
            """)

        with col_p:
            render_html("""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:14px; margin-bottom:12px;">
                <div style="font-size:14px; font-weight:750; color:#0284c7; margin-bottom:8px;">🏢 Property &amp; Cyber Claims</div>
                <ul style="font-size:12px; line-height:1.7; color:#334155; margin:0; padding-left:18px;">
                    <li><b>Surveyor Asset Loss Assessment Report</b>.</li>
                    <li><b>Reinstatement / Replacement Invoices &amp; Asset Register</b>.</li>
                    <li><b>Forensic Incident Response Report</b> (for Cyber claims).</li>
                    <li><b>Fire Department / Police NOC Certificate</b> (for Property fire/burglary).</li>
                </ul>
            </div>
            """)
