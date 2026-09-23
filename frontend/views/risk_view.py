"""
Risk, Fraud & MCP Integrations View for InsurAgent enterprise UI.
"""
import streamlit as st
import pandas as pd
import textwrap
from backend.client import insuragent_client


def render_risk_view() -> None:
    st.markdown('<div class="page-title">Enterprise System Integrations &amp; Fraud Risk Services</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Standardized Model Context Protocol (MCP) tool integration layer connecting core insurance systems.</div>', unsafe_allow_html=True)

    # ---------- 4 Core Enterprise System Integrations ----------
    st.markdown("##### 🔌 Enterprise MCP System Integrations")

    integrations = [
        {
            "Service Name": "Policy Administration System (PAS)",
            "Connection Status": "● Connected",
            "Tool Name": "get_policy_details(policy_number)",
            "Last Called": "2026-09-23 18:05:12",
            "Response Status": "Successful (200 OK)",
            "Execution Time": "45 ms"
        },
        {
            "Service Name": "Claims Database & Repository",
            "Connection Status": "● Connected",
            "Tool Name": "get_claim_details(claim_id)",
            "Last Called": "2026-09-23 18:05:15",
            "Response Status": "Successful (200 OK)",
            "Execution Time": "40 ms"
        },
        {
            "Service Name": "Customer Information System (CRM)",
            "Connection Status": "● Connected",
            "Tool Name": "get_customer_details(customer_id)",
            "Last Called": "2026-09-23 18:04:40",
            "Response Status": "Successful (200 OK)",
            "Execution Time": "38 ms"
        },
        {
            "Service Name": "Fraud & Risk Intelligence Service",
            "Connection Status": "● Connected",
            "Tool Name": "get_risk_indicators(claim_id)",
            "Last Called": "2026-09-23 18:05:18",
            "Response Status": "Successful (200 OK)",
            "Execution Time": "85 ms"
        }
    ]

    st.dataframe(pd.DataFrame(integrations), use_container_width=True, hide_index=True)

    st.write("")

    # ---------- Live Fraud & Anomaly Test Sandbox ----------
    with st.container(border=True):
        st.markdown("##### 🔎 Fraud Bureau & Risk Indicator Inspector")
        st.markdown("Query the MCP Fraud Detection Bureau to inspect loss ratio anomalies, rapid inception flags, and provider risk scores.")

        c1, c2 = st.columns([4, 1.2])
        with c1:
            test_claim_id = st.text_input("Enter Claim ID for Risk Screening", value="CLM-20260918-B81C")
        with c2:
            run_risk = st.button("Query Risk Bureau", type="primary", use_container_width=True)

        if run_risk and test_claim_id:
            with st.spinner("Invoking MCP Fraud Detection Service..."):
                risk_res = insuragent_client.execute_mcp_tool("get_risk_indicators", {"claim_id": test_claim_id.strip()})

            if risk_res.get("success"):
                score = risk_res.get("risk_score", 0.12)
                cat = risk_res.get("risk_category", "Low Risk")
                flags = risk_res.get("indicators", [])

                badge_cls = "badge-red" if score >= 0.60 else ("badge-amber" if score >= 0.40 else "badge-green")

                st.markdown(textwrap.dedent(f"""
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px; margin-top:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <span style="font-size:14px; font-weight:800; color:#0f172a;">Risk Bureau Profile: {test_claim_id}</span>
                        <div style="display:flex; gap:6px;">
                            <span class="status-badge {badge_cls}">Risk Category: {cat}</span>
                            <span class="status-badge badge-navy">Risk Score: {score:.2f}</span>
                        </div>
                    </div>
                    <div style="font-size:12px; font-weight:700; color:#0f172a; margin-bottom:4px;">Risk Indicators &amp; Anomaly Signals:</div>
                </div>
                """), unsafe_allow_html=True)

                for f in flags:
                    st.markdown(f"<div style='font-size:12px; color:#64748b; margin-bottom:3px;'>• {f}</div>", unsafe_allow_html=True)
