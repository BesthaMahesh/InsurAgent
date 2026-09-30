"""
Executive Operations Dashboard View for InsurAgent enterprise UI.
Combines executive KPI cards, Altair data visualizations,
live query synthesis, and active claims operations queue.
"""
import streamlit as st
import pandas as pd
import textwrap
from backend.client import insuragent_client
from backend.services.claim_service import ClaimService
from frontend.components.cards import render_kpi_card
from frontend.components.charts import (
    render_claims_trend_chart,
    render_claims_status_distribution,
    render_risk_distribution_chart,
    render_ai_vs_human_chart,
    render_agent_latency_chart
)
from frontend.components.adjudication_panel import render_adjudication_panel


def render_dashboard_view() -> None:
    st.markdown('<div class="page-title">Claims Intelligence Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Real-time enterprise analytics, autonomous claims adjudication, risk distribution, and operational metrics.</div>', unsafe_allow_html=True)

    # ---------- Row 1: Top 6 Executive KPI Cards ----------
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        render_kpi_card("Total Claims", "863", "100% Tracked", "All Lines", "blue", trend_text="12 today", trend_positive=True)
    with k2:
        render_kpi_card("In Review", "18", "Pending adjuster check", "Action Needed", "amber")
    with k3:
        render_kpi_card("AI-Assisted", "845", "97.9% straight-through", "Automated", "green")
    with k4:
        render_kpi_card("Human Escalated", "18", "2.1% HITL routing rate", "Within SLA", "navy")
    with k5:
        render_kpi_card("Fraud / Risk Flags", "12", "1.4% anomalous claims", "MCP Screened", "red")
    with k6:
        render_kpi_card("Avg Processing Time", "480 ms", "Sub-second multi-agent DAG", "Fast Track", "blue")

    st.write("")

    # ---------- Row 2: Charts - Trend & Status Distribution ----------
    c_trend, c_status = st.columns([1.6, 1])
    with c_trend:
        with st.container(border=True):
            render_claims_trend_chart()
    with c_status:
        with st.container(border=True):
            render_claims_status_distribution()

    st.write("")

    # ---------- Row 3: Charts - Risk Distribution & AI vs Human Processing ----------
    c_risk, c_ai_human = st.columns([1.3, 1.3])
    with c_risk:
        with st.container(border=True):
            render_risk_distribution_chart()
    with c_ai_human:
        with st.container(border=True):
            render_ai_vs_human_chart()

    st.write("")

    # ---------- Row 4: Processing Latency by Agent & Operations Telemetry ----------
    c_lat, c_agents = st.columns([1.4, 1.2])
    with c_lat:
        with st.container(border=True):
            render_agent_latency_chart()
    with c_agents:
        with st.container(border=True):
            st.markdown("<div style='font-size:13.5px; font-weight:750; color:#0f172a; margin-bottom:2px;'>6 Specialized Collaborative Agents</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:11.5px; color:#64748b; margin-bottom:8px;'>LangGraph autonomous expert workers.</div>", unsafe_allow_html=True)

            agents = [
                ("1. Claim Intake Agent", "Classify line & validate completeness", "Healthy"),
                ("2. Document Analysis Agent", "Vision-OCR extraction & invoice check", "Healthy"),
                ("3. Policy Verification Agent", "Coverage check & ChromaDB RAG", "Healthy"),
                ("4. Fraud / Risk Analysis Agent", "Anomaly detection & MCP Bureau", "Healthy"),
                ("5. Claim Assessment Agent", "Calculate payout & evaluate HITL", "Healthy"),
                ("6. Audit & Compliance Agent", "IRDAI compliance & cryptographic seal", "Healthy")
            ]
            for name, role, st_val in agents:
                st.markdown(textwrap.dedent(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; padding:4px 0; border-bottom:1px solid #f8fafc; font-size:11.5px;">
                    <div>
                        <span style="font-weight:700; color:#0f172a;">{name}</span>
                        <div style="font-size:10px; color:#64748b;">{role}</div>
                    </div>
                    <span class="status-badge badge-green" style="font-size:9.5px;">● {st_val}</span>
                </div>
                """), unsafe_allow_html=True)

    st.write("")

    # ---------- Main Query Area: "Ask InsurAgent" ----------
    with st.container(border=True):
        st.markdown(textwrap.dedent("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div>
                <div style="font-size:15px; font-weight:800; color:#0f172a;">🔍 Ask InsurAgent</div>
                <div style="font-size:12px; color:#64748b;">Analyze claims, verify policy clauses, evaluate coverage rules, or check anomaly indicators.</div>
            </div>
            <span class="status-badge badge-blue">● LangGraph Orchestrator Connected</span>
        </div>
        """), unsafe_allow_html=True)

        st.markdown("<div style='font-size:11px;font-weight:700;color:#64748b;margin-bottom:6px;'>EXAMPLE ENTERPRISE QUERIES:</div>", unsafe_allow_html=True)
        p1, p2, p3, p4 = st.columns(4)
        preset_query = None

        with p1:
            if st.button("✈️ Travel Shield limits & perils", use_container_width=True, key="dash_btn_1"):
                preset_query = "What are the covered perils and maximum payout limits for trip cancellation under the Travel Shield policy?"
        with p2:
            if st.button("⚠️ Explain human review need", use_container_width=True, key="dash_btn_2"):
                preset_query = "Explain why claim CLM-20260918-B81C requires human review and identify all risk indicators."
        with p3:
            if st.button("📋 Gold Health waiting period", use_container_width=True, key="dash_btn_3"):
                preset_query = "What is the waiting period applicable to pre-existing diseases under the Gold Health Policy?"
        with p4:
            if st.button("🏥 Check claim coverage (A12F)", use_container_width=True, key="dash_btn_4"):
                preset_query = "Check whether claim CLM-20260918-A12F is covered under the policy and explain why."

        q_col, btn_col = st.columns([5, 1.2])
        with q_col:
            user_query = st.text_input(
                "Ask InsurAgent Input",
                value=preset_query if preset_query else (st.session_state.get("dash_user_query") or ""),
                placeholder="Ask about a claim, policy coverage, risk, documents or compliance...",
                label_visibility="collapsed",
                key="dash_query_input_box"
            )

        with btn_col:
            analyze_clicked = st.button("Analyze", type="primary", use_container_width=True, key="dash_exec_analyze")

        # Handle Execution
        if (analyze_clicked or preset_query) and user_query.strip():
            progress_placeholder = st.empty()
            with progress_placeholder.container():
                st.markdown(textwrap.dedent("""
                <div style="background:#ffffff; border:1px solid #bfdbfe; border-radius:10px; padding:14px 16px; margin-top:12px; box-shadow:0 2px 6px rgba(2,132,199,0.05);">
                    <div style="display:flex; align-items:center; gap:8px; font-weight:800; font-size:13.5px; color:#0369a1;">
                        <span style="font-size:16px;">⏳</span> InsurAgent is analyzing policy and claim intelligence...
                    </div>
                    <div style="margin-top:8px; font-size:11.5px; color:#475569; display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                        <span class="status-badge badge-blue">Input Guardrails</span> →
                        <span class="status-badge badge-blue">Claim Intake</span> →
                        <span class="status-badge badge-blue">Document Analysis</span> →
                        <span class="status-badge badge-blue">Policy RAG</span> →
                        <span class="status-badge badge-blue">Risk Analysis</span> →
                        <span class="status-badge badge-blue">Claim Assessment</span> →
                        <span class="status-badge badge-blue">Audit Seal</span> →
                        <span class="status-badge badge-green">Output Guardrails</span>
                    </div>
                </div>
                """), unsafe_allow_html=True)

            try:
                chat_res = insuragent_client.post_chat(user_query)
                progress_placeholder.empty()
                if chat_res and not chat_res.get("error"):
                    st.session_state["dash_user_query"] = user_query
                    st.session_state["dash_chat_response"] = chat_res
                    st.session_state["dash_error"] = None
                else:
                    st.session_state["dash_error"] = chat_res.get("error", "Unable to complete request.")
            except Exception as ex:
                progress_placeholder.empty()
                st.session_state["dash_error"] = str(ex)

        if st.session_state.get("dash_error"):
            st.error(f"Error: {st.session_state['dash_error']}")

        # Render Dynamic AI Adjudication & Evidence Synthesis Panel
        if st.session_state.get("dash_user_query") and st.session_state.get("dash_chat_response") and not st.session_state.get("dash_error"):
            render_adjudication_panel(
                st.session_state["dash_chat_response"],
                st.session_state.get("dash_user_query", "")
            )

    st.write("")

    # ---------- Recent Claims Queue Table ----------
    with st.container(border=True):
        st.markdown("<div style='font-size:14.5px; font-weight:750; color:#0f172a; margin-bottom:2px;'>Recent Claims Operations Queue</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:12px; color:#64748b; margin-bottom:10px;'>Active claims processed across multi-agent adjudication workflows.</div>", unsafe_allow_html=True)

        recent_claims = ClaimService.list_recent_claims(limit=10)
        if recent_claims:
            df_recent = pd.DataFrame(recent_claims)
            display_df = df_recent[["claim_id", "claimant_name", "claim_type", "policy_number", "amount", "status", "recommendation"]]
            display_df.columns = ["Claim ID", "Claimant", "Line", "Policy", "Amount (₹)", "Status", "AI Recommendation"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No claims currently in the queue.")
