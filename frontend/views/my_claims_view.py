"""
My Claims View for InsurAgent End User Experience.
Provides policyholders and adjusters with a clean list of their claims,
status badges, payout details, and quick inspection actions.
"""
import streamlit as st
import pandas as pd
from backend.services.claim_service import ClaimService
from frontend.components.claim_view import render_claim_overview
from frontend.styles import render_html


def render_my_claims_view() -> None:
    """Renders the My Claims tracking and management workspace."""
    render_html('<div class="page-title">My Claims</div>')
    render_html('<div class="page-subtitle">Track and manage all registered insurance claims, active reviews, and settlement payouts.</div>')

    # Fetch live database claims
    all_claims = ClaimService.list_recent_claims(limit=50)

    # Filter controls
    f1, f2, f3 = st.columns([2, 1.5, 1.5])
    with f1:
        search_kw = st.text_input("Search Claims", placeholder="Search by Claim ID, Claimant, or Policy Number...", label_visibility="collapsed", key="my_claims_search_input")
    with f2:
        line_filter = st.selectbox("Line of Business", ["All Lines", "Health", "Motor", "Travel", "Property", "Cyber"], label_visibility="collapsed", key="my_claims_line_filter")
    with f3:
        status_filter = st.selectbox("Claim Status", ["All Statuses", "Completed", "In Review", "Escalated"], label_visibility="collapsed", key="my_claims_status_filter")

    filtered = []
    for c in all_claims:
        match_kw = True
        if search_kw:
            q = search_kw.lower()
            match_kw = (q in c["claim_id"].lower() or q in c["claimant_name"].lower() or q in c["policy_number"].lower())
        match_line = (line_filter == "All Lines" or c["claim_type"] == line_filter)
        match_status = (status_filter == "All Statuses" or c["status"] == status_filter)

        if match_kw and match_line and match_status:
            filtered.append(c)

    st.write("")

    if not filtered:
        st.info("No claims matching your search criteria.")
        return

    # Render summary table
    table_rows = []
    for c in filtered:
        table_rows.append({
            "Claim ID": c["claim_id"],
            "Claimant": c["claimant_name"],
            "Line": c["claim_type"],
            "Policy": c["policy_number"],
            "Amount": f"₹{c['amount']:,.2f}",
            "Date": c.get("incident_date") or c.get("created_at", ""),
            "Status": c["status"],
            "Recommendation": c["recommendation"]
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

    st.write("")
    st.markdown("##### 🔍 Quick Inspect Claim Record")
    c_sel, c_btn = st.columns([4, 1.2])
    with c_sel:
        target_claim_id = st.selectbox(
            "Select Claim to Inspect",
            [c["claim_id"] for c in filtered],
            format_func=lambda cid: f"{cid} — {[c['claimant_name'] for c in filtered if c['claim_id']==cid][0]} (₹{[c['amount'] for c in filtered if c['claim_id']==cid][0]:,.2f})",
            label_visibility="collapsed",
            key="my_claims_target_select"
        )
    with c_btn:
        if st.button("👁️ View Full File", type="primary", use_container_width=True, key="my_claims_view_btn"):
            st.session_state["active_claim_id"] = target_claim_id
            st.session_state["active_nav_page"] = "Claims"
            st.rerun()

    st.write("")
    # Render preview of selected claim
    st.markdown(f"##### 📄 Claim Overview Preview: `{target_claim_id}`")
    c_data = ClaimService.get_claim(target_claim_id)
    if c_data:
        render_claim_overview(c_data)
