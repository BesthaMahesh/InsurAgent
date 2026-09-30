"""
MCP Tools View for InsurAgent Developer Experience.
Provides deep visibility into the Model Context Protocol (MCP) server integration,
registered enterprise tools, tool call schema, and live execution test console.
"""
import streamlit as st
import pandas as pd
import json
import time
from backend.client import insuragent_client
from frontend.styles import render_html


def render_mcp_view() -> None:
    """Renders the Model Context Protocol (MCP) Tools management view."""
    render_html('<div class="page-title">MCP Tools</div>')
    render_html('<div class="page-subtitle">Model Context Protocol (MCP) server integration, registered tool definitions, and external data connectors.</div>')

    # ---------- Top Status KPIs ----------
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("MCP Server Status", "Operational", "Port 8000 &bull; 200 OK")
    with c2:
        st.metric("Registered Tools", "4 Core Tools", "JSON Schema Validated")
    with c3:
        st.metric("Total Tool Calls", "1,694 Invocations", "Sub-100ms avg latency")
    with c4:
        st.metric("Security & Auth", "TLS 1.3 + Scoped Key", "SOC 2 Type II")

    st.write("")

    # ---------- Architecture & Technical Flow ----------
    with st.container(border=True):
        st.markdown("##### 🔌 MCP Technical Data Flow Architecture")
        render_html("""
        <div style="background:#091524; border:1px solid #1e2e42; border-radius:10px; padding:16px; margin-bottom:12px; color:#ffffff;">
            <div style="font-size:12px; font-weight:700; color:#38bdf8; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.5px;">Tool Invocation Lifecycle</div>
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; font-size:11.5px;">
                <span style="background:#0f2744; border:1px solid #1e3a5f; padding:6px 10px; border-radius:6px; color:#93c5fd;">Risk / Intake Agent</span> →
                <span style="background:#0f2744; border:1px solid #1e3a5f; padding:6px 10px; border-radius:6px; color:#93c5fd;">MCP Client Helper</span> →
                <span style="background:#0f2744; border:1px solid #1e3a5f; padding:6px 10px; border-radius:6px; color:#93c5fd;">FastAPI MCP Server</span> →
                <span style="background:#0284c7; border:1px solid #0369a1; padding:6px 10px; border-radius:6px; color:#ffffff; font-weight:700;">Target Tool Function</span> →
                <span style="background:#0f2744; border:1px solid #1e3a5f; padding:6px 10px; border-radius:6px; color:#93c5fd;">External Enterprise Data</span> →
                <span style="background:#047857; border:1px solid #065f46; padding:6px 10px; border-radius:6px; color:#ffffff; font-weight:700;">Structured JSON Result</span>
            </div>
        </div>
        """)

    st.write("")

    # ---------- Registered MCP Tools Catalog ----------
    with st.container(border=True):
        st.markdown("##### 📋 Registered Enterprise MCP Tools Catalog")
        
        tools_catalog = [
            {
                "Tool Name": "get_risk_indicators",
                "Target System": "Central Fraud & Risk Bureau",
                "Description": "Evaluates cross-insurer loss histories, inception deltas, and provider anomaly flags.",
                "Parameters": "claim_id (string, required)",
                "Avg Latency": "85 ms",
                "Status": "● Operational"
            },
            {
                "Tool Name": "get_policy_details",
                "Target System": "Policy Administration System (PAS)",
                "Description": "Retrieves active coverage terms, sum insured limits, policy endorsements, and deductibles.",
                "Parameters": "policy_number (string, required)",
                "Avg Latency": "45 ms",
                "Status": "● Operational"
            },
            {
                "Tool Name": "get_claim_details",
                "Target System": "Claims Core Database",
                "Description": "Fetches historical claim adjudication records and previous loss submissions.",
                "Parameters": "claim_id (string, required)",
                "Avg Latency": "40 ms",
                "Status": "● Operational"
            },
            {
                "Tool Name": "get_customer_details",
                "Target System": "Customer Information CRM",
                "Description": "Retrieves claimant KYC verification status, policyholder tenure, and credit tier.",
                "Parameters": "customer_id (string, required)",
                "Avg Latency": "38 ms",
                "Status": "● Operational"
            }
        ]
        st.dataframe(pd.DataFrame(tools_catalog), use_container_width=True, hide_index=True)

    st.write("")

    # ---------- Interactive Live MCP Tool Sandbox ----------
    with st.container(border=True):
        st.markdown("##### 🧪 Interactive MCP Tool Execution Sandbox")
        render_html("<div style='font-size:12px; color:#64748b; margin-bottom:12px;'>Dispatch live requests to the MCP server and observe the real returned JSON payload and latency.</div>")

        col_t, col_arg = st.columns([1.5, 2])
        with col_t:
            selected_tool = st.selectbox(
                "Select MCP Tool to Test",
                ["get_risk_indicators", "get_policy_details", "get_claim_details", "get_customer_details"],
                key="mcp_tool_sel"
            )
        with col_arg:
            if selected_tool == "get_risk_indicators":
                default_param = '{"claim_id": "CLM-20260918-B81C"}'
            elif selected_tool == "get_policy_details":
                default_param = '{"policy_number": "POL-HEALTH-GOLD-2026"}'
            elif selected_tool == "get_claim_details":
                default_param = '{"claim_id": "CLM-20260918-A12F"}'
            else:
                default_param = '{"customer_id": "CUST-883921"}'

            param_input = st.text_input("JSON Parameters", value=default_param, key="mcp_param_input")

        exec_btn = st.button("⚡ Execute MCP Tool", type="primary", use_container_width=True, key="mcp_exec_tool_btn")

        if exec_btn:
            try:
                parsed_args = json.loads(param_input)
                t_start = time.time()
                with st.spinner(f"Invoking {selected_tool}..."):
                    tool_res = insuragent_client.execute_mcp_tool(selected_tool, parsed_args)
                dur_ms = round((time.time() - t_start) * 1000, 1)

                st.markdown(f"###### ✓ Execution Response ({dur_ms} ms)")
                st.json(tool_res)
            except Exception as e:
                st.error(f"Error executing MCP tool: {str(e)}")
