"""
Claims Workspace View for InsurAgent enterprise UI.
"""
import streamlit as st
from datetime import datetime
import uuid
import base64
from backend.client import insuragent_client
from frontend.components.claim_view import render_claim_overview
from frontend.components.timeline import render_claim_processing_timeline, render_audit_trace_timeline


def render_claims_view() -> None:
    st.markdown('<div class="page-title">Claims Management Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Submit, track, investigate, and review claims across multi-agent adjudication workflows.</div>', unsafe_allow_html=True)

    tab_new, tab_list, tab_detail = st.tabs(["📝 Submit New Claim", "📋 Claims Repository", "🔍 Claim Details & Timeline"])

    with tab_new:
        with st.form("enterprise_claim_submission_form", clear_on_submit=False):
            st.markdown("##### 👤 Claimant Profile & Policy Identification")
            c1, c2, c3 = st.columns(3)
            with c1:
                name = st.text_input("Claimant Full Name", value="Mahesh Sharma")
            with c2:
                email = st.text_input("Email Address", value="mahesh.sharma@example.com")
            with c3:
                policy_no = st.text_input("Policy Number", value="POL-HEALTH-GOLD-2026")

            st.markdown("##### 📄 Incident Particulars & Line of Business")
            c1, c2, c3 = st.columns(3)
            with c1:
                line = st.selectbox("Insurance Line", ["Health", "Motor", "Travel", "Property", "Cyber"])
            with c2:
                amt = st.number_input("Claim Amount (₹)", min_value=0.0, value=125000.0, step=5000.0)
            with c3:
                inc_date = st.date_input("Incident Date")

            desc = st.text_area(
                "Clinical / Incident Description & Hospital/Workshop Records",
                height=90,
                value="Emergency inpatient hospitalization for acute appendicitis. 3-day continuous hospital stay with laparoscopic appendectomy performed at Apollo Multispeciality Hospital."
            )

            attached_files = st.file_uploader(
                "Attach Invoices, Bills, Estimates or Discharge Summaries",
                type=["pdf", "png", "jpg", "jpeg", "txt"],
                accept_multiple_files=True
            )

            submitted = st.form_submit_button("🚀 Submit Claim to Multi-Agent Pipeline", type="primary", use_container_width=True)

        if submitted:
            if not name or not policy_no or not desc:
                st.error("Please fill in Claimant Name, Policy Number, and Incident Description.")
            else:
                new_id = f"CLM-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}"
                st.session_state["active_claim_id"] = new_id

                doc_list = []
                if attached_files:
                    for f in attached_files:
                        b64 = base64.b64encode(f.read()).decode("utf-8")
                        doc_list.append({"filename": f.name, "file_type": f.name.split(".")[-1], "content_base64": b64})

                payload = {
                    "claim_id": new_id,
                    "persona": st.session_state.get("current_persona", "Claims Adjuster"),
                    "claimant": {"name": name, "email": email or "", "phone": ""},
                    "claim_details": {
                        "policy_number": policy_no,
                        "claim_type": line,
                        "amount": float(amt),
                        "incident_date": str(inc_date),
                        "description": desc
                    },
                    "documents": doc_list
                }

                with st.spinner("Processing through 6 LangGraph Autonomous Agents..."):
                    res = insuragent_client.process_claim(payload)
                    st.session_state["latest_claim_result"] = res

                st.success(f"Claim `{new_id}` processed successfully!")
                
                # Render Overview and Timelines
                render_claim_overview({
                    "claim_id": new_id,
                    "claimant_name": name,
                    "claim_type": line,
                    "policy_number": policy_no,
                    "amount": amt,
                    "status": res.get("status", "Completed"),
                    "risk_level": res.get("risk_analysis", {}).get("risk_level", "Low Risk"),
                    "recommendation": res.get("assessment", {}).get("recommendation", "Recommended for Approval"),
                    "confidence": res.get("assessment", {}).get("confidence", 0.90),
                    "description": desc
                })

                render_claim_processing_timeline(8)

                if res.get("audit_events"):
                    render_audit_trace_timeline(res["audit_events"], trace_id=res.get("trace_id"))

    with tab_list:
        st.markdown("##### Registered Enterprise Claims Database")
        sample_repo = [
            {"Claim ID": "CLM-20260918-A12F", "Claimant": "Mahesh Sharma", "Line": "Health", "Policy": "POL-HEALTH-GOLD-2026", "Amount": "₹1,25,000", "Status": "Completed", "Risk": "Low Risk"},
            {"Claim ID": "CLM-20260918-B81C", "Claimant": "Priya Patel", "Line": "Motor", "Policy": "POL-MOTOR-COMP-2026", "Amount": "₹82,500", "Status": "Escalated", "Risk": "Requires Investigation"},
            {"Claim ID": "CLM-20260918-C42D", "Claimant": "Ananya Roy", "Line": "Health", "Policy": "POL-HEALTH-GOLD-2026", "Amount": "₹2,10,000", "Status": "In Review", "Risk": "Medium Risk"},
            {"Claim ID": "CLM-20260917-D73A", "Claimant": "Rahul Verma", "Line": "Travel", "Policy": "POL-TRAVEL-SHIELD-2026", "Amount": "₹45,000", "Status": "Completed", "Risk": "Low Risk"}
        ]
        st.dataframe(sample_repo, use_container_width=True, hide_index=True)

    with tab_detail:
        st.markdown("##### Inspect Claim Details by ID")
        c_id = st.text_input("Enter Claim ID to Inspect", value=st.session_state.get("active_claim_id", "CLM-20260918-A12F"))
        
        if st.button("Load Claim File", type="primary"):
            c_data = insuragent_client.get_claim(c_id)
            if not c_data:
                # Use standard realistic demo data for CLM-20260918-A12F
                c_data = {
                    "claim_id": c_id,
                    "claimant_name": "Mahesh Sharma",
                    "claim_type": "Health",
                    "policy_number": "POL-HEALTH-GOLD-2026",
                    "amount": 125000.0,
                    "status": "Completed",
                    "risk_level": "Low Risk",
                    "recommendation": "Recommended for Approval",
                    "confidence": 0.90,
                    "description": "Emergency inpatient hospitalization for acute appendicitis with laparoscopic appendectomy."
                }
            render_claim_overview(c_data)
            render_claim_processing_timeline(8)
            events = insuragent_client.get_audit_trail(c_id)
            render_audit_trace_timeline(events, trace_id=f"TRC-{c_id[-6:]}")
