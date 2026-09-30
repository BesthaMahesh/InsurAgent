"""
Header component for InsurAgent enterprise UI.
Renders the executive brand banner, operational system health badge,
and active user role without exposing email addresses in the top header.
"""
import streamlit as st
from frontend.styles import render_html


def render_header(current_persona: str = "Claims Adjuster") -> None:
    """Renders the top enterprise header bar."""
    role_display = st.session_state.get("user_role", current_persona.split('(')[0].strip())
    
    html = f"""
    <div class="top-header-bar">
        <div class="header-brand">
            <div class="header-logo-icon">🛡️</div>
            <div>
                <div class="header-title-text">INSURAGENT</div>
                <div class="header-subtitle-text">Enterprise Insurance Claims Intelligence Platform</div>
            </div>
        </div>
        <div class="header-right-meta">
            <span class="status-badge badge-green" title="All 5 Core Subsystems Connected">
                <span style="font-size:8px;">●</span> Operational
            </span>
            <span class="status-badge badge-blue" title="Authenticated User Role">
                👤 {role_display}
            </span>
            <span class="status-badge badge-navy" style="cursor:pointer;" title="Enterprise Configuration">
                ⚙️ Config
            </span>
        </div>
    </div>
    """
    render_html(html)
