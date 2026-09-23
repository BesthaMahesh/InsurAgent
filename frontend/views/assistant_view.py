"""
AI Claims Assistant View for InsurAgent enterprise UI.
"""
import time
import textwrap
import streamlit as st
from backend.client import insuragent_client
from frontend.components.adjudication_panel import render_adjudication_panel


def render_assistant_view() -> None:
    st.markdown('<div class="page-title">AI Claims Intelligence Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Natural language query engine grounded in ChromaDB policy repository, MCP Bureau, and multi-agent reasoning.</div>', unsafe_allow_html=True)

    # ---------- Main Search & Query Container ----------
    with st.container(border=True):
        st.markdown(textwrap.dedent("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div>
                <div style="font-size:14px; font-weight:800; color:#0f172a;">🔍 Ask InsurAgent</div>
                <div style="font-size:12px; color:#64748b;">Analyze claims, identify risk indicators, verify policy clauses, or check compliance.</div>
            </div>
            <span class="status-badge badge-blue">● LangGraph Orchestrator Connected</span>
        </div>
        """), unsafe_allow_html=True)

        st.markdown("<div style='font-size:11px; font-weight:700; color:#64748b; margin-bottom:6px;'>EXAMPLE ENTERPRISE QUERIES:</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            q1 = st.button("✈️ 1. Travel Shield: Trip cancellation covered perils & limits", use_container_width=True)
            q2 = st.button("⚠️ 2. Explain why claim requires human review (CLM-20260918-B81C)", use_container_width=True)
            q3 = st.button("📋 3. Check Gold Health pre-existing disease waiting period", use_container_width=True)
        with c2:
            q4 = st.button("🔍 4. Identify risk indicators for claim CLM-20260918-B81C", use_container_width=True)
            q5 = st.button("🏥 5. Check policy coverage for claim CLM-20260918-A12F", use_container_width=True)

        selected_example = None
        if q1:
            selected_example = "What are the covered perils and maximum payout limits for trip cancellation under the Travel Shield policy?"
        elif q2:
            selected_example = "Explain why claim CLM-20260918-B81C requires human review and identify all risk indicators."
        elif q3:
            selected_example = "What is the waiting period applicable to pre-existing diseases under the Gold Health Policy?"
        elif q4:
            selected_example = "Explain why claim CLM-20260918-B81C requires human review and identify all risk indicators."
        elif q5:
            selected_example = "Check whether claim CLM-20260918-A12F is covered under the policy and explain why."


        st.write("")
        q_text, btn_col = st.columns([5, 1.2])
        with q_text:
            current_val = selected_example if selected_example else (st.session_state.get("asst_query") or "Explain why claim CLM-20260918-B81C requires human review and identify all risk indicators.")
            query_val = st.text_input(
                "Natural Language Query",
                value=current_val,
                placeholder="Ask about claim coverage, exclusions, deductible rules, or risk flags...",
                label_visibility="collapsed",
                key="asst_query_input"
            )
        with btn_col:
            submit_query = st.button("Analyze", type="primary", use_container_width=True, key="asst_analyze_btn")

        # Handle Execution with Enterprise Loading State
        if (submit_query or selected_example) and query_val.strip():
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
                res = insuragent_client.post_chat(query_val)
                progress_placeholder.empty()
                if res and not res.get("error"):
                    st.session_state["asst_query"] = query_val
                    st.session_state["asst_response"] = res
                    st.session_state["asst_error"] = None
                else:
                    st.session_state["asst_error"] = res.get("error", "Unable to complete request.")
            except Exception as ex:
                progress_placeholder.empty()
                st.session_state["asst_error"] = str(ex)

        # ---------- Error Handling State ----------
        if st.session_state.get("asst_error"):
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
            if st.button("🔄 Try Again", key="asst_try_again"):
                st.session_state["asst_error"] = None
                st.rerun()

        # ---------- Dynamic AI Adjudication & Evidence Synthesis Panel ----------
        if st.session_state.get("asst_response") and not st.session_state.get("asst_error"):
            render_adjudication_panel(
                st.session_state["asst_response"],
                st.session_state.get("asst_query", "")
            )
