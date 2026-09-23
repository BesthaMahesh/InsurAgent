"""
INSURAGENT
Enterprise Multi-Agent Claims Intelligence & Audit Platform
"Smarter Claims. Fairer Decisions. Greater Trust."
"""
import streamlit as st
from frontend.styles import ENTERPRISE_CSS
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.views import (
    render_dashboard_view,
    render_claims_view,
    render_assistant_view,
    render_workflow_view,
    render_rag_view,
    render_risk_view,
    render_human_review_view,
    render_audit_view,
    render_governance_view,
    render_evaluation_view,
    render_cost_view,
    render_monitoring_view
)

# 1. Streamlit Application Configuration
st.set_page_config(
    page_title="InsurAgent | Enterprise Claims Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Enterprise Stylesheet
st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)

# 3. Sidebar Navigation & Active Persona
selected_page, current_persona = render_sidebar()

# 4. Top Executive Brand Header Bar
render_header(current_persona=current_persona)

# 5. Page Dispatcher
if selected_page == "Dashboard":
    render_dashboard_view()
elif selected_page == "Claims":
    render_claims_view()
elif selected_page == "AI Assistant":
    render_assistant_view()
elif selected_page == "Multi-Agent Workflow":
    render_workflow_view()
elif selected_page == "Knowledge / RAG":
    render_rag_view()
elif selected_page == "Risk & Fraud":
    render_risk_view()
elif selected_page == "Human Review":
    render_human_review_view()
elif selected_page == "Audit & Traceability":
    render_audit_view()
elif selected_page == "Governance & Responsible AI":
    render_governance_view()
elif selected_page == "Model Evaluation":
    render_evaluation_view()
elif selected_page == "Cost & Usage":
    render_cost_view()
elif selected_page == "System Monitoring":
    render_monitoring_view()
else:
    render_dashboard_view()
