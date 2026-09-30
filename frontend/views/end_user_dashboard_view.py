"""
End-User Claims Intelligence Dashboard View for InsurAgent.
Provides a clean, business-focused claims intelligence workspace.
Zero technical clutter, strictly real data from SQLite and backend services.
"""
import streamlit as st
import pandas as pd
from backend.services.claim_service import ClaimService
from frontend.components.cards import render_kpi_card
from frontend.components.charts import (
    render_claims_status_distribution,
    render_claims_trend_chart
)
from frontend.styles import render_html


def render_end_user_dashboard_view() -> None:
    """Renders the business-facing Claims Intelligence Dashboard."""
    render_html('<div class="page-title">Claims Intelligence Dashboard</div>')
    render_html('<div class="page-subtitle">Manage claims, track processing and get assistance with your insurance coverage.</div>')

    # Fetch real claims data from database
    recent_claims = ClaimService.list_recent_claims(limit=50)
    total_claims_count = len(recent_claims)
    in_review_count = sum(1 for c in recent_claims if c.get("status") == "In Review")
    completed_count = sum(1 for c in recent_claims if c.get("status") == "Completed")
    action_required_count = sum(1 for c in recent_claims if c.get("requires_human_review") or c.get("status") == "Escalated")

    # ---------- Row 1: Business-Focused KPI Cards ----------
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("My Claims", str(total_claims_count), "All registered claims", "Active", "blue")
    with k2:
        render_kpi_card("Claims In Review", str(in_review_count), "Under adjuster assessment", "In Progress", "amber")
    with k3:
        render_kpi_card("Completed Claims", str(completed_count), "Settled & processed", "Settled", "green")
    with k4:
        render_kpi_card("Action Required", str(action_required_count), "Additional info / review needed", "Action Needed", "red" if action_required_count > 0 else "green")

    st.write("")

    # ---------- Row 2: Quick Action Bar ----------
    with st.container(border=True):
        st.markdown("<div style='font-size:13.5px; font-weight:750; color:#0f172a; margin-bottom:8px;'>⚡ Quick Actions</div>", unsafe_allow_html=True)
        qa1, qa2, qa3 = st.columns(3)
        with qa1:
            if st.button("📝 Submit New Claim", use_container_width=True, type="primary", key="user_dash_submit_btn"):
                st.session_state["active_nav_page"] = "Claims"
                st.session_state["user_nav_radio"] = "📋  Claims"
                st.rerun()
        with qa2:
            if st.button("💬 Ask Policy Assistant", use_container_width=True, key="user_dash_ask_btn"):
                st.session_state["active_nav_page"] = "AI Assistant"
                st.session_state["user_nav_radio"] = "💬  AI Assistant"
                st.rerun()
        with qa3:
            if st.button("📚 View Policy Guidelines", use_container_width=True, key="user_dash_kc_btn"):
                st.session_state["active_nav_page"] = "Knowledge Center"
                st.session_state["user_nav_radio"] = "📚  Knowledge Center"
                st.rerun()

    st.write("")

    # ---------- Row 3: Business Analytics Charts ----------
    c_trend, c_dist = st.columns([1.5, 1])
    with c_trend:
        with st.container(border=True):
            render_claims_trend_chart()
    with c_dist:
        with st.container(border=True):
            render_claims_status_distribution()

    st.write("")

    # ---------- Row 4: Recent Claims Table with [View] Action ----------
    with st.container(border=True):
        st.markdown("<div style='font-size:15px; font-weight:750; color:#0f172a; margin-bottom:2px;'>Recent Claims</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:12px; color:#64748b; margin-bottom:12px;'>Track the status and outcome of recent claims registered in the system.</div>", unsafe_allow_html=True)

        if recent_claims:
            table_rows = []
            for c in recent_claims:
                table_rows.append({
                    "Claim ID": c["claim_id"],
                    "Claimant": c.get("claimant_name", ""),
                    "Line": c.get("claim_type", ""),
                    "Date": c.get("incident_date") or c.get("created_at", ""),
                    "Amount": f"₹{c['amount']:,.2f}",
                    "Policy": c.get("policy_number", ""),
                    "Status": c.get("status", "Completed"),
                    "Recommendation": c.get("recommendation", "Recommended for Approval")
                })
            
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

            st.write("")
            st.markdown("##### 🔍 Inspect Claim Details")
            col_sel, col_act = st.columns([4, 1.2])
            with col_sel:
                selected_claim_id = st.selectbox(
                    "Select Claim to Inspect",
                    [c["claim_id"] for c in recent_claims],
                    format_func=lambda cid: f"{cid} — {[c['claimant_name'] for c in recent_claims if c['claim_id']==cid][0]} (₹{[c['amount'] for c in recent_claims if c['claim_id']==cid][0]:,.2f})",
                    label_visibility="collapsed",
                    key="user_dash_claim_select"
                )
            with col_act:
                if st.button("👁️ View Claim Details", type="primary", use_container_width=True, key="user_dash_view_btn"):
                    st.session_state["active_claim_id"] = selected_claim_id
                    st.session_state["active_nav_page"] = "Claims"
                    st.session_state["user_nav_radio"] = "📋  Claims"
                    st.rerun()
        else:
            st.info("No claims found in the database.")

