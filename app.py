"""
INSURAGENT
Enterprise Insurance Claims Intelligence Platform
"Smarter Claims. Fairer Decisions. Greater Trust."
"""
import streamlit as st
from backend.database.database import init_db
from backend.services.claim_service import ClaimService
from frontend.styles import ENTERPRISE_CSS
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.views import (
    render_login_view,
    render_dashboard_view,
    render_claims_view,
    render_evaluation_view,
    render_cost_view,
    render_assistant_view,
    render_usage_view,
    render_workflow_view,
    render_rag_view,
    render_risk_view,
    render_human_review_view,
    render_audit_view,
    render_governance_view,
    render_monitoring_view
)

# 1. Streamlit Application Configuration
st.set_page_config(
    page_title="InsurAgent | Enterprise Claims Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Database & Sample Schema Initialization
init_db()
ClaimService.seed_default_claims()

# 3. Inject Enterprise Stylesheet
st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)

# 4. Enterprise Authentication Gate
if not st.session_state.get("authenticated", False):
    render_login_view()
    st.stop()

# 5. Sidebar Navigation & Active Persona
selected_page, current_persona = render_sidebar()

# 6. Top Executive Brand Header Bar
render_header(current_persona=current_persona)

# 7. Enterprise Page Dispatcher (All 13 Client-Facing & Operations Pages)
if selected_page == "Dashboard":
    render_dashboard_view()
elif selected_page == "Claims":
    render_claims_view()
elif selected_page == "Model Evaluation":
    render_evaluation_view()
elif selected_page == "Cost Analysis":
    render_cost_view()
elif selected_page == "AI Assistant":
    render_assistant_view()
elif selected_page == "Usage & Tokens":
    render_usage_view()
elif selected_page == "Processing Workflow":
    render_workflow_view()
elif selected_page == "Knowledge Center":
    render_rag_view()
elif selected_page == "Risk & Fraud":
    render_risk_view()
elif selected_page == "Human Review":
    render_human_review_view()
elif selected_page == "Audit & Compliance":
    render_audit_view()
elif selected_page == "Trust & Responsible AI":
    render_governance_view()
elif selected_page == "System Health":
    render_monitoring_view()
else:
    render_dashboard_view()
