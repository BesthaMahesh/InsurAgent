"""
Dashboard Dispatcher View for InsurAgent enterprise UI.
Routes to Developer Technical Operations Dashboard or End User Claims Intelligence Dashboard
based on authenticated session role.
"""
import streamlit as st
from frontend.views.end_user_dashboard_view import render_end_user_dashboard_view
from frontend.views.developer_dashboard_view import render_developer_dashboard_view


def render_dashboard_view() -> None:
    """Renders the appropriate dashboard based on authenticated role."""
    role_type = st.session_state.get("role_type", "claims_adjuster")
    if role_type == "developer":
        render_developer_dashboard_view()
    else:
        render_end_user_dashboard_view()

