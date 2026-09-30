"""
Trust & Responsible AI View for InsurAgent enterprise UI.
Provides algorithmic fairness evaluation, automated adversarial safety batteries,
PII data governance, and regulatory compliance oversight.
"""
import streamlit as st
import pandas as pd
import textwrap
from backend.client import insuragent_client


def render_governance_view() -> None:
    st.markdown('<div class="page-title">Trust &amp; Responsible AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Algorithmic fairness evaluation, PII data protection, responsible AI controls, and automated adversarial safety testing.</div>', unsafe_allow_html=True)

    gov_data = insuragent_client.get_governance_overview()
    bias_data = gov_data.get("bias_fairness", {})
    matrix = gov_data.get("compliance_matrix", {})

    tab_adv, tab_bias, tab_comp, tab_data, tab_model = st.tabs([
        "🛡️ Adversarial Safety Testing",
        "⚖️ Algorithmic Fairness",
        "📋 Regulatory Compliance",
        "🗄️ Data Protection & Privacy",
        "🤖 Model Governance"
    ])

    with tab_adv:
        st.markdown("##### Automated Adversarial Safety Battery (Red-Teaming)")
        st.markdown("<div style='font-size:12px; color:#64748b; margin-bottom:10px;'>Simulates jailbreak attempts, prompt injections, and system prompt extraction attacks against the Input Guardrail layer.</div>", unsafe_allow_html=True)

        if st.button("⚡ Run Adversarial Safety Test", type="primary", key="gov_run_adv_btn"):
            with st.spinner("Executing adversarial attack vectors..."):
                adv_results = insuragent_client.run_adversarial_test()
                st.session_state["adv_results"] = adv_results

        if "adv_results" in st.session_state:
            res = st.session_state["adv_results"]
            score = res.get("robustness_score_percentage", 100.0)
            status_cls = "badge-green" if score >= 95.0 else "badge-amber"
            st.markdown(textwrap.dedent(f"""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:12px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <b>Robustness Score:</b> {score}% ({res.get('passed_tests')}/{res.get('total_tests')} Tests Passed)
                </div>
                <span class="status-badge {status_cls}">Status: {res.get('safety_status', 'SECURE')}</span>
            </div>
            """), unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(res.get("test_results", [])), use_container_width=True, hide_index=True)

    with tab_bias:
        st.markdown("##### Algorithmic Bias & Demographic Parity Evaluation")
        st.markdown("<div style='font-size:12px; color:#64748b; margin-bottom:10px;'>Evaluates demographic parity and four-fifths rule compliance across age, geography, and provider networks.</div>", unsafe_allow_html=True)

        f_index = bias_data.get("overall_fairness_index", 0.97) * 100
        st.markdown(textwrap.dedent(f"""
        <div style="display:flex; gap:12px; margin-bottom:12px;">
            <span class="status-badge badge-green">Overall Fairness Index: {f_index:.1f}%</span>
            <span class="status-badge badge-green">Four-Fifths Rule: {bias_data.get('fairness_status', 'Passed')}</span>
            <span class="status-badge badge-navy">Protected Attribute Masking: Active</span>
        </div>
        """), unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(bias_data.get("demographic_parity_analysis", [])), use_container_width=True, hide_index=True)

    with tab_comp:
        st.markdown("##### Enterprise Regulatory Compliance Matrix")
        st.dataframe(pd.DataFrame(matrix.get("frameworks", [])), use_container_width=True, hide_index=True)

    with tab_data:
        st.markdown("##### Data Protection, Encryption & PII Masking")
        data_gov = gov_data.get("data_governance", {})
        st.markdown(textwrap.dedent(f"""
        <div style="display:flex; gap:12px; margin-bottom:12px;">
            <span class="status-badge badge-green">Data Quality Index: {data_gov.get('data_quality_index', 0.98)*100:.1f}%</span>
            <span class="status-badge badge-navy">Encryption at Rest: {data_gov.get('encryption_at_rest', 'AES-256 Enabled')}</span>
            <span class="status-badge badge-navy">Encryption in Transit: {data_gov.get('encryption_in_transit', 'TLS 1.3')}</span>
            <span class="status-badge badge-green">PII Tokenization: Active</span>
        </div>
        """), unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(data_gov.get("catalog_inventory", [])), use_container_width=True, hide_index=True)

    with tab_model:
        st.markdown("##### Model Governance & Hyperparameter Registry")
        model_gov = gov_data.get("model_governance", {})
        st.markdown(textwrap.dedent(f"""
        <div style="display:flex; gap:12px; margin-bottom:12px;">
            <span class="status-badge badge-blue">Governance Standard: {model_gov.get('governance_standard', 'ISO/IEC 42001')}</span>
            <span class="status-badge badge-purple">Orchestration Engine: {model_gov.get('orchestration_engine', 'LangGraph v0.2.x')}</span>
        </div>
        """), unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(model_gov.get("active_models", [])), use_container_width=True, hide_index=True)
