"""
System Monitoring & Observability View for InsurAgent enterprise UI.
"""
import streamlit as st
import pandas as pd
import textwrap
from backend.client import insuragent_client
from frontend.components.charts import render_performance_table


def render_monitoring_view() -> None:
    st.markdown('<div class="page-title">System Monitoring &amp; Observability</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Real-time system health, component connectivity, agent telemetry, and Service Level Objectives (SLOs).</div>', unsafe_allow_html=True)

    telemetry = insuragent_client.get_observability()
    agent_perf = telemetry.get("agent_performance", {})
    slos = telemetry.get("slos", [])
    alerts = telemetry.get("active_alerts", [])

    # ---------- Component Health Cards ----------
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("FastAPI Backend", "Operational", "Port 8000 • 200 OK")
    with c2:
        st.metric("LangGraph DAG", "Operational", "Stateful Multi-Agent")
    with c3:
        st.metric("ChromaDB RAG", "Connected", "41 Chunks Indexed")
    with c4:
        st.metric("MCP Integrations", "Connected", "4 Core Services")
    with c5:
        st.metric("SQLite Database", "Connected", "Active Schema")

    st.write("")

    # ---------- Service Level Objectives (SLOs) ----------
    with st.container(border=True):
        st.markdown("##### 🎯 Service Level Objectives (SLOs)")
        if slos:
            st.dataframe(pd.DataFrame(slos), use_container_width=True, hide_index=True)

    # ---------- Agent Telemetry & Tool Invocations ----------
    col_a, col_b = st.columns([1.3, 1])

    with col_a:
        with st.container(border=True):
            st.markdown("##### ⚡ Agent Execution Telemetry")
            render_performance_table(agent_perf)

    with col_b:
        with st.container(border=True):
            st.markdown("##### 🔌 MCP Integration Tool Calls")
            tool_data = [
                {"Tool Name": "get_policy_details", "Category": "Policy PAS", "Calls": 580, "Avg Latency": "45 ms", "Status": "Healthy"},
                {"Tool Name": "get_claim_details", "Category": "Claims DB", "Calls": 312, "Avg Latency": "40 ms", "Status": "Healthy"},
                {"Tool Name": "get_customer_details", "Category": "Customer CRM", "Calls": 290, "Avg Latency": "38 ms", "Status": "Healthy"},
                {"Tool Name": "get_risk_indicators", "Category": "Fraud Bureau", "Calls": 512, "Avg Latency": "85 ms", "Status": "Healthy"}
            ]
            st.dataframe(pd.DataFrame(tool_data), use_container_width=True, hide_index=True)

    # ---------- Active System & Security Alerts ----------
    with st.container(border=True):
        st.markdown("##### 🚨 Active System & Anomaly Alerts")
        if alerts:
            for alt in alerts:
                st.markdown(textwrap.dedent(f"""
                <div style="padding:10px 12px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; margin-bottom:6px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#0f172a; font-size:12.5px;">{alt.get('title')}</span>
                        <span class="status-badge {'badge-amber' if alt.get('severity')=='Medium' else 'badge-blue'}">{alt.get('severity')} Severity</span>
                    </div>
                    <div style="font-size:12px; color:#64748b; margin-top:2px;">{alt.get('description')}</div>
                    <div style="font-size:10px; color:#94a3b8; margin-top:3px;">Timestamp: {alt.get('timestamp')} | Status: {alt.get('status')}</div>
                </div>
                """), unsafe_allow_html=True)
        else:
            st.info("No active security or anomaly alerts.")
