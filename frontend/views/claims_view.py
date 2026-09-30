"""
Claims Management View for InsurAgent enterprise UI.
Implements:
1. Structured Submit New Claim form with MANDATORY supporting document upload validation.
2. Enterprise Claims Repository table with search filters and interactive [View] action.
3. Comprehensive Claim Details viewer with complete adjudication sections and previous claims history.
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import base64
from backend.client import insuragent_client
from backend.services.claim_service import ClaimService
from frontend.components.claim_view import render_claim_overview
from frontend.components.timeline import render_claim_processing_timeline, render_audit_trace_timeline
from frontend.styles import render_html


def render_claims_view() -> None:
    st.markdown('<div class="page-title">Claims Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Submit, track, and review insurance claims across autonomous multi-agent adjudication workflows.</div>', unsafe_allow_html=True)

    tab_new, tab_list, tab_detail = st.tabs(["📝 Submit New Claim", "📋 Claims Repository", "🔍 Claim Details"])

    # ==========================================
    # TAB 1: SUBMIT NEW CLAIM
    # ==========================================
    with tab_new:
        submit_card_html = """
        <div class="enterprise-card" style="margin-bottom:14px;">
            <div class="card-title">Submit Insurance Claim</div>
            <div class="card-subtitle">Complete claimant information, incident particulars, and upload mandatory supporting documentation.</div>
        </div>
        """
        render_html(submit_card_html)

        # Section 1: Claimant Information
        st.markdown("##### 👤 1. Claimant Information")
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("Claimant Full Name *", value="Mahesh Sharma", key="claim_form_name")
        with c2:
            email = st.text_input("Email Address", value="mahesh.sharma@example.com", key="claim_form_email")
        with c3:
            policy_no = st.text_input("Policy Number *", value="POL-HEALTH-GOLD-2026", key="claim_form_policy")

        # Section 2: Incident Particulars
        st.markdown("##### 📄 2. Incident Details & Line of Business")
        c1, c2, c3 = st.columns(3)
        with c1:
            line = st.selectbox("Insurance Line *", ["Health", "Motor", "Travel", "Property", "Cyber"], key="claim_form_line")
        with c2:
            amt = st.number_input("Claim Amount (₹) *", min_value=100.0, value=125000.0, step=5000.0, key="claim_form_amt")
        with c3:
            inc_date = st.date_input("Incident Date *", key="claim_form_date")

        desc = st.text_area(
            "Clinical / Incident Description & Hospital/Workshop Records *",
            height=90,
            value="Emergency inpatient hospitalization for acute appendicitis. 3-day continuous hospital stay with laparoscopic appendectomy performed at Apollo Multispeciality Hospital.",
            key="claim_form_desc"
        )

        # Section 3: Supporting Documents (MANDATORY)
        st.markdown("##### 📎 3. Supporting Documents (Mandatory)")
        st.markdown("<div style='font-size:12px; color:#64748b; margin-bottom:8px;'>Supporting documentation (Hospital Bill, Invoice, Discharge Summary, Medical Report, or Repair Estimate) is strictly required before submission.</div>", unsafe_allow_html=True)

        attached_files = st.file_uploader(
            "Upload Supporting Documentation",
            type=["pdf", "png", "jpg", "jpeg", "txt"],
            accept_multiple_files=True,
            help="Mandatory: Upload invoices, bills, discharge summaries or estimates.",
            key="claim_form_uploader"
        )

        # File preview & status validation indicator
        if attached_files:
            st.markdown(f"<div style='font-size:12px; font-weight:700; color:#047857; margin-top:6px;'>✓ {len(attached_files)} document(s) staged for ingestion</div>", unsafe_allow_html=True)
            for f in attached_files:
                size_kb = round(f.size / 1024, 1)
                file_chip_html = f"""
                <div class="file-chip">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span>📄</span>
                        <span style="font-weight:600; color:#0f172a;">{f.name}</span>
                        <span style="color:#64748b; font-size:11px;">({size_kb} KB)</span>
                    </div>
                    <span class="status-badge badge-green">✓ Ready</span>
                </div>
                """
                render_html(file_chip_html)
        else:
            warn_html = """
            <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:10px 14px; margin-top:6px; font-size:12px; color:#92400e; display:flex; align-items:center; gap:8px;">
                <span>⚠️</span> <b>Supporting documentation is required before submitting this claim.</b> Please attach at least one invoice, medical report, or bill.
            </div>
            """
            render_html(warn_html)

        st.write("")
        submit_btn = st.button("🚀 Submit Claim for Adjudication", type="primary", use_container_width=True, key="submit_claim_action_btn")

        if submit_btn:
            # Mandatory Document & Field Validation
            if not attached_files:
                st.error("Supporting documentation is required before submitting this claim. Please upload at least one supporting document (PDF, PNG, JPG, or TXT).")
            elif not name.strip() or not policy_no.strip() or not desc.strip():
                st.error("Please complete all mandatory fields: Claimant Full Name, Policy Number, and Incident Description.")
            else:
                new_id = f"CLM-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:4].upper()}"
                st.session_state["active_claim_id"] = new_id

                doc_list = []
                for f in attached_files:
                    b64 = base64.b64encode(f.getvalue()).decode("utf-8")
                    doc_list.append({
                        "filename": f.name,
                        "file_type": f.name.split(".")[-1],
                        "content_base64": b64
                    })

                payload = {
                    "claim_id": new_id,
                    "persona": st.session_state.get("current_persona", "Claims Adjuster (Employee)"),
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

                with st.spinner("Executing 6-Agent LangGraph Adjudication Workflow..."):
                    res = insuragent_client.process_claim(payload)
                    st.session_state["latest_claim_result"] = res

                    # Save record to SQLite
                    assessment_data = res.get("assessment", {})
                    assessment_data["documents"] = [d["filename"] for d in doc_list]
                    ClaimService.save_or_update_claim(
                        claim_id=new_id,
                        claimant_name=name,
                        email=email or "",
                        policy_number=policy_no,
                        claim_type=line,
                        amount=float(amt),
                        description=desc,
                        incident_date=str(inc_date),
                        status=res.get("status", "Completed"),
                        recommendation=assessment_data.get("recommendation", "Recommended for Approval"),
                        confidence=res.get("confidence", 0.90),
                        requires_human_review=res.get("requires_human_review", False),
                        human_review_reason=res.get("human_review_reason"),
                        assessment_data=assessment_data
                    )

                st.success(f"Claim `{new_id}` submitted and processed successfully!")

                # Direct View Claim Action
                v_col1, v_col2 = st.columns([1.5, 4])
                with v_col1:
                    if st.button(f"🔍 Inspect Claim File ({new_id})", type="primary", key="view_just_submitted"):
                        st.session_state["active_claim_id"] = new_id
                        st.rerun()

                st.write("")
                # Render Processing Progress Lifecycle
                render_claim_processing_timeline(8)

                # Render Full Overview
                render_claim_overview({
                    "claim_id": new_id,
                    "claimant_name": name,
                    "email": email,
                    "claim_type": line,
                    "policy_number": policy_no,
                    "amount": amt,
                    "status": res.get("status", "Completed"),
                    "risk_level": res.get("risk_analysis", {}).get("risk_level", "Low Risk"),
                    "risk_score": res.get("risk_analysis", {}).get("risk_score", 0.12),
                    "recommendation": res.get("assessment", {}).get("recommendation", "Recommended for Approval"),
                    "confidence": res.get("assessment", {}).get("confidence", 0.90),
                    "description": desc,
                    "documents": doc_list,
                    "audit_events": res.get("audit_events", [])
                })

    # ==========================================
    # TAB 2: CLAIMS REPOSITORY
    # ==========================================
    with tab_list:
        repo_header_html = """
        <div class="enterprise-card" style="margin-bottom:12px;">
            <div class="card-title">Enterprise Claims Repository</div>
            <div class="card-subtitle">Search, filter, and inspect registered claims across all lines of insurance.</div>
        </div>
        """
        render_html(repo_header_html)

        # Filters
        f1, f2, f3 = st.columns([2, 1.5, 1.5])
        with f1:
            search_text = st.text_input("Search Claims by ID, Claimant, or Policy", placeholder="e.g. Mahesh, POL-HEALTH, CLM-...", label_visibility="collapsed", key="repo_search_box")
        with f2:
            filter_line = st.selectbox("Filter Line", ["All Lines", "Health", "Motor", "Travel", "Property", "Cyber"], label_visibility="collapsed", key="repo_filter_line")
        with f3:
            filter_status = st.selectbox("Filter Status", ["All Statuses", "Completed", "In Review", "Escalated"], label_visibility="collapsed", key="repo_filter_status")

        # Fetch live database claims
        all_claims = ClaimService.list_recent_claims(limit=50)
        filtered_claims = []
        for c in all_claims:
            match_search = True
            if search_text:
                q = search_text.lower()
                match_search = (q in c["claim_id"].lower() or q in c["claimant_name"].lower() or q in c["policy_number"].lower())
            
            match_line = (filter_line == "All Lines" or c["claim_type"] == filter_line)
            match_status = (filter_status == "All Statuses" or c["status"] == filter_status)

            if match_search and match_line and match_status:
                filtered_claims.append(c)

        if filtered_claims:
            table_data = []
            for c in filtered_claims:
                risk_tag = "Requires Investigation" if c.get("requires_human_review") else "Low Risk"
                table_data.append({
                    "Claim ID": c["claim_id"],
                    "Claimant": c["claimant_name"],
                    "Insurance Line": c["claim_type"],
                    "Policy": c["policy_number"],
                    "Claim Amount": f"₹{c['amount']:,.2f}",
                    "Date": c.get("incident_date") or c.get("created_at"),
                    "Status": c["status"],
                    "Risk": risk_tag
                })
            st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

            st.write("")
            st.markdown("##### 🔍 Actions: Quick Inspect Claim")
            c_select_col, c_btn_col = st.columns([4, 1.2])
            with c_select_col:
                selected_claim_id = st.selectbox(
                    "Select Claim to View",
                    [c["claim_id"] for c in filtered_claims],
                    format_func=lambda cid: f"{cid} — {[c['claimant_name'] for c in filtered_claims if c['claim_id']==cid][0]} (₹{[c['amount'] for c in filtered_claims if c['claim_id']==cid][0]:,.0f})",
                    label_visibility="collapsed",
                    key="repo_quick_select"
                )
            with c_btn_col:
                if st.button("👁️ View Claim Details", type="primary", use_container_width=True, key="repo_view_action"):
                    st.session_state["active_claim_id"] = selected_claim_id
                    st.toast(f"Loading claim record {selected_claim_id}...", icon="📋")
                    st.rerun()
        else:
            st.info("No claims matching your filter criteria.")

    # ==========================================
    # TAB 3: CLAIM DETAILS
    # ==========================================
    with tab_detail:
        current_inspect_id = st.session_state.get("active_claim_id", "CLM-20260918-A12F")
        
        c_in1, c_in2 = st.columns([4, 1.2])
        with c_in1:
            inspect_id = st.text_input("Enter Claim ID to Inspect", value=current_inspect_id, label_visibility="collapsed", key="claim_detail_lookup_input")
        with c_in2:
            if st.button("Load File", type="primary", use_container_width=True, key="claim_detail_load_btn"):
                st.session_state["active_claim_id"] = inspect_id.strip()
                st.rerun()

        claim_data = ClaimService.get_claim(inspect_id.strip())
        if claim_data:
            render_claim_overview(claim_data)
        else:
            st.warning(f"Claim `{inspect_id}` not found in the database. Please verify the ID or select from the Claims Repository.")
