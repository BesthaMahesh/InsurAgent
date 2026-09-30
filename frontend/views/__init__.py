"""InsurAgent Enterprise UI Views."""
from frontend.views.login_view import render_login_view
from frontend.views.dashboard_view import render_dashboard_view
from frontend.views.end_user_dashboard_view import render_end_user_dashboard_view
from frontend.views.developer_dashboard_view import render_developer_dashboard_view
from frontend.views.claims_view import render_claims_view
from frontend.views.assistant_view import render_assistant_view
from frontend.views.my_claims_view import render_my_claims_view
from frontend.views.documents_view import render_documents_view
from frontend.views.knowledge_center_view import render_knowledge_center_view
from frontend.views.help_support_view import render_help_support_view
from frontend.views.workflow_view import render_workflow_view
from frontend.views.rag_view import render_rag_view
from frontend.views.mcp_view import render_mcp_view
from frontend.views.guardrails_view import render_guardrails_view
from frontend.views.risk_view import render_risk_view
from frontend.views.human_review_view import render_human_review_view
from frontend.views.audit_view import render_audit_view
from frontend.views.governance_view import render_governance_view
from frontend.views.evaluation_view import render_evaluation_view
from frontend.views.cost_view import render_cost_view
from frontend.views.usage_view import render_usage_view
from frontend.views.monitoring_view import render_monitoring_view
from frontend.views.logs_view import render_logs_view

__all__ = [
    "render_login_view",
    "render_dashboard_view",
    "render_end_user_dashboard_view",
    "render_developer_dashboard_view",
    "render_claims_view",
    "render_assistant_view",
    "render_my_claims_view",
    "render_documents_view",
    "render_knowledge_center_view",
    "render_help_support_view",
    "render_workflow_view",
    "render_rag_view",
    "render_mcp_view",
    "render_guardrails_view",
    "render_risk_view",
    "render_human_review_view",
    "render_audit_view",
    "render_governance_view",
    "render_evaluation_view",
    "render_cost_view",
    "render_usage_view",
    "render_monitoring_view",
    "render_logs_view"
]

