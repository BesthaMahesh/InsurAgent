"""
Executive Operations Dashboard View for InsurAgent enterprise UI.
"""
import streamlit as st
import textwrap
from backend.client import insuragent_client
from frontend.components.cards import render_kpi_card
from frontend.components.workflow import render_workflow_diagram
from frontend.components.adjudication_panel import render_adjudication_panel


def render_dashboard_view() -> None:
    st.markdown('<div class="page-title">Claims Intelligence Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Real-time visibility into claims, AI decisions, risk, compliance and auditability.</div>', unsafe_allow_html=True)

    # ---------- 8 Top KPI Cards ----------
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Total Claims", "863", "863 ingested polycontexts", "100% Tracked", "blue")
    with k2:
        render_kpi_card("Claims in Review", "18", "Pending adjuster check", "Action Needed", "amber")
    with k3:
        render_kpi_card("AI-Assisted Decisions", "845", "97.9% auto-adjudicated", "● Automated", "green")
    with k4:
        render_kpi_card("Human Escalations", "18", "2.1% HITL routing rate", "Within SLA", "navy")

    k5, k6, k7, k8 = st.columns(4)
    with k5:
        render_kpi_card("Fraud / Risk Flags", "12", "1.4% flagged anomalies", "MCP Screened", "red")
    with k6:
        render_kpi_card("RAG Grounding", "98.2%", "Zero policy hallucination", "Grounded", "purple")
    with k7:
        render_kpi_card("Audit Coverage", "100.0%", "Immutable SQLite & Token", "IRDAI Sealed", "green")
    with k8:
        render_kpi_card("Avg Processing Time", "480 ms", "Sub-second multi-agent DAG", "Fast Track", "blue")

    st.write("")

    # ---------- Main Prominent Search / Query Area: "Ask InsurAgent" ----------
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
            if st.button("✈️ 1. Travel Shield limits & perils", use_container_width=True):
                preset_query = "What are the covered perils and maximum payout limits for trip cancellation under the Travel Shield policy?"
        with p2:
            if st.button("⚠️ 2. Explain human review need", use_container_width=True):
                preset_query = "Explain why claim CLM-20260918-B81C requires human review and identify all risk indicators."
        with p3:
            if st.button("📋 3. Gold Health waiting period", use_container_width=True):
                preset_query = "What is the waiting period applicable to pre-existing diseases under the Gold Health Policy?"
        with p4:
            if st.button("🏥 4. Check claim coverage (A12F)", use_container_width=True):
                preset_query = "Check whether claim CLM-20260918-A12F is covered under the policy and explain why."


        q_col, btn_col = st.columns([5, 1.2])
        with q_col:
            user_query = st.text_input(
                "Ask InsurAgent Input",
                value=preset_query if preset_query else (st.session_state.get("query_result") or ""),
                placeholder="Ask about a claim, policy coverage, risk, documents or compliance...",
                label_visibility="collapsed"
            )

        with btn_col:
            analyze_clicked = st.button("Analyze", type="primary", use_container_width=True)

        # Handle Execution with Enterprise Loading State
        if (analyze_clicked or preset_query) and user_query.strip():
            progress_placeholder = st.empty()
            with progress_placeholder.container():
                st.markdown(textwrap.dedent("""
                <div style="background:#ffffff; border:1px solid #bfdbfe; border-radius:10px; padding:16px; margin-top:12px; box-shadow:0 2px 6px rgba(2,132,199,0.05);">
                    <div style="display:flex; align-items:center; gap:10px; font-weight:800; font-size:14px; color:#0369a1;">
                        <span style="font-size:18px;">⏳</span> InsurAgent is analyzing the claim...
                    </div>
                    <div style="margin-top:10px; font-size:12px; color:#475569; display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                        <span class="status-badge badge-blue">Input Guardrails</span> →
                        <span class="status-badge badge-blue">Claim Intake</span> →
                        <span class="status-badge badge-blue">Document Analysis</span> →
                        <span class="status-badge badge-blue">Policy RAG</span> →
                        <span class="status-badge badge-blue">Risk Analysis</span> →
                        <span class="status-badge badge-blue">Claim Assessment</span> →
                        <span class="status-badge badge-blue">Audit &amp; Compliance</span> →
                        <span class="status-badge badge-green">Output Guardrails</span>
                    </div>
                </div>
                """), unsafe_allow_html=True)

            try:
                chat_res = insuragent_client.post_chat(user_query)
                progress_placeholder.empty()
                if chat_res and not chat_res.get("error"):
                    st.session_state["query_result"] = user_query
                    st.session_state["chat_response"] = chat_res
                    st.session_state["dash_error"] = None
                else:
                    st.session_state["dash_error"] = chat_res.get("error", "Unable to complete request.")
            except Exception as ex:
                progress_placeholder.empty()
                st.session_state["dash_error"] = str(ex)

        if st.session_state.get("dash_error"):
            st.markdown(textwrap.dedent("""
            <div style="background:#fef2f2; border:1px solid #fecaca; border-left:4px solid #ef4444; border-radius:8px; padding:14px 16px; margin-top:14px;">
                <div style="font-weight:800; font-size:14px; color:#991b1b; display:flex; align-items:center; gap:8px;">
                    ❌ Unable to process the claim
                </div>
                <div style="font-size:12px; color:#7f1d1d; margin-top:4px;">
                    We encountered an issue communicating with the multi-agent backend service. Please check your network connection or try again.
                </div>
            </div>
            """), unsafe_allow_html=True)

        # Render Dynamic AI Adjudication & Evidence Synthesis Panel
        if st.session_state.get("query_result") and st.session_state.get("chat_response") and not st.session_state.get("dash_error"):
            render_adjudication_panel(
                st.session_state["chat_response"],
                st.session_state.get("query_result", "")
            )


    st.write("")

    # ---------- Recent Claims Queue & Multi-Agent Status ----------
    c_left, c_right = st.columns([1.6, 1])

    with c_left:
        with st.container(border=True):
            st.markdown("<div style='font-size:14px; font-weight:750; color:#0f172a; margin-bottom:2px;'>Recent Claims Queue</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:11.5px; color:#64748b; margin-bottom:10px;'>Active claims flowing through multi-agent adjudication.</div>", unsafe_allow_html=True)
            
            queue_data = [
                {"Claim ID": "CLM-20260918-A12F", "Claimant": "Mahesh Sharma", "Line": "Health", "Amount": "₹1,25,000", "AI Recommendation": "Recommended for Approval", "Status": "Completed"},
                {"Claim ID": "CLM-20260918-B81C", "Claimant": "Priya Patel", "Line": "Motor", "Amount": "₹82,500", "AI Recommendation": "Requires Investigation", "Status": "Escalated ⚠️"},
                {"Claim ID": "CLM-20260918-C42D", "Claimant": "Ananya Roy", "Line": "Health", "Amount": "₹2,10,000", "AI Recommendation": "Missing Document Check", "Status": "In Review ⚠️"},
                {"Claim ID": "CLM-20260917-D73A", "Claimant": "Rahul Verma", "Line": "Travel", "Amount": "₹45,000", "AI Recommendation": "Approved for Settlement", "Status": "Completed"}
            ]
            st.dataframe(queue_data, use_container_width=True, hide_index=True)

    with c_right:
        with st.container(border=True):
            st.markdown("<div style='font-size:14px; font-weight:750; color:#0f172a; margin-bottom:2px;'>6 Specialized Collaborative Agents</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:11.5px; color:#64748b; margin-bottom:8px;'>LangGraph autonomous expert workers.</div>", unsafe_allow_html=True)

            agents = [
                ("1. Claim Intake Agent", "Classify line & validate completeness", "Healthy"),
                ("2. Document Analysis Agent", "OCR extraction & invoice check", "Healthy"),
                ("3. Policy Verification Agent", "Coverage check & Chroma RAG", "Healthy"),
                ("4. Fraud / Risk Analysis Agent", "Anomaly detection & MCP Bureau", "Healthy"),
                ("5. Claim Assessment Agent", "Calculate payout & evaluate HITL", "Healthy"),
                ("6. Audit & Compliance Agent", "IRDAI compliance & audit seal", "Healthy")
            ]
            for name, role, st_val in agents:
                st.markdown(textwrap.dedent(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; padding:5px 0; border-bottom:1px solid #f8fafc; font-size:11.5px;">
                    <div>
                        <span style="font-weight:700; color:#0f172a;">{name}</span>
                        <div style="font-size:9.5px; color:#64748b;">{role}</div>
                    </div>
                    <span class="status-badge badge-green" style="font-size:9.5px;">● {st_val}</span>
                </div>
                """), unsafe_allow_html=True)

    # Render Visual Workflow Diagram
    render_workflow_diagram()
