"""
INSURAGENT
Enterprise Insurance Claims Intelligence Platform
"Smarter Claims. Fairer Decisions. Greater Trust."
"""
import os
import sys

# 1. Disable ChromaDB & PostHog telemetry to eliminate cloud container network hangs
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# 2. Linux SQLite patch for ChromaDB on Streamlit Community Cloud
try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

import streamlit as st
from frontend.styles import ENTERPRISE_CSS

# 3. Streamlit Application Configuration
st.set_page_config(
    page_title="InsurAgent | Enterprise Claims Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 4. Inject Enterprise Stylesheet
st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)

# 5. Fast-Path Enterprise Authentication Gate (Zero Heavy Imports When Logged Out)
if not st.session_state.get("authenticated", False):
    from frontend.views.login_view import render_login_view
    render_login_view()
    st.stop()

# 6. Database & Sample Schema Initialization (Cached: Runs ONCE, never blocks reruns)
@st.cache_resource(show_spinner=False)
def ensure_database_initialized():
    try:
        from backend.database.database import init_db
        from backend.services.claim_service import ClaimService
        init_db()
        ClaimService.seed_default_claims()
    except Exception as e:
        import logging
        logging.getLogger("InsurAgent").warning(f"Database init warning: {e}")
    return True

ensure_database_initialized()

# 7. Authenticated Layout Components
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar

# 8. Enforce role consistency strictly from authenticated email
user_email = (st.session_state.get("user_email") or "").strip().lower()
if user_email in ("wrenchwisedevoloper@gmail.com", "wrenchwisedeveloper@gmail.com"):
    st.session_state["role_type"] = "developer"
    st.session_state["user_role"] = "Developer / Technical Operations"
    role_type = "developer"
else:
    st.session_state["role_type"] = "claims_adjuster"
    st.session_state["user_role"] = "Claims Adjuster"
    role_type = "claims_adjuster"

# 9. Sidebar Navigation & Active Persona
selected_page, current_persona = render_sidebar()

# 10. Top Executive Brand Header Bar
render_header(current_persona=current_persona)

# 11. Role-Based On-Demand Page Dispatcher (Lazy Loaded for Peak Performance)
if role_type == "developer":
    if selected_page == "Technical Dashboard":
        from frontend.views.developer_dashboard_view import render_developer_dashboard_view
        render_developer_dashboard_view()
    elif selected_page == "Agent Workflow":
        from frontend.views.workflow_view import render_workflow_view
        render_workflow_view()
    elif selected_page == "Knowledge / RAG":
        from frontend.views.rag_view import render_rag_view
        render_rag_view()
    elif selected_page == "MCP Tools":
        from frontend.views.mcp_view import render_mcp_view
        render_mcp_view()
    elif selected_page == "Guardrails":
        from frontend.views.guardrails_view import render_guardrails_view
        render_guardrails_view()
    elif selected_page == "Human-in-the-Loop":
        from frontend.views.human_review_view import render_human_review_view
        render_human_review_view()
    elif selected_page == "Model Evaluation":
        from frontend.views.evaluation_view import render_evaluation_view
        render_evaluation_view()
    elif selected_page == "Cost Analytics":
        from frontend.views.cost_view import render_cost_view
        render_cost_view()
    elif selected_page == "Token Usage":
        from frontend.views.usage_view import render_usage_view
        render_usage_view()
    elif selected_page == "Audit & Traceability":
        from frontend.views.audit_view import render_audit_view
        render_audit_view()
    elif selected_page == "System Health":
        from frontend.views.monitoring_view import render_monitoring_view
        render_monitoring_view()
    elif selected_page == "Execution Logs":
        from frontend.views.logs_view import render_logs_view
        render_logs_view()
    elif selected_page == "Claims":
        from frontend.views.claims_view import render_claims_view
        render_claims_view()
    elif selected_page == "Risk & Fraud":
        from frontend.views.risk_view import render_risk_view
        render_risk_view()
    else:
        from frontend.views.developer_dashboard_view import render_developer_dashboard_view
        render_developer_dashboard_view()
else:
    # End User / Claims Adjuster Experience
    if selected_page == "Dashboard":
        from frontend.views.end_user_dashboard_view import render_end_user_dashboard_view
        render_end_user_dashboard_view()
    elif selected_page == "Claims":
        from frontend.views.claims_view import render_claims_view
        render_claims_view()
    elif selected_page == "AI Assistant":
        from frontend.views.assistant_view import render_assistant_view
        render_assistant_view()
    elif selected_page == "My Claims":
        from frontend.views.my_claims_view import render_my_claims_view
        render_my_claims_view()
    elif selected_page == "Documents":
        from frontend.views.documents_view import render_documents_view
        render_documents_view()
    elif selected_page == "Knowledge Center":
        from frontend.views.knowledge_center_view import render_knowledge_center_view
        render_knowledge_center_view()
    elif selected_page == "Help & Support":
        from frontend.views.help_support_view import render_help_support_view
        render_help_support_view()
    else:
        from frontend.views.end_user_dashboard_view import render_end_user_dashboard_view
        render_end_user_dashboard_view()
