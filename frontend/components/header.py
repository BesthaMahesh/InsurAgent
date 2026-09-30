"""
Header component for InsurAgent enterprise UI.
Renders the executive brand banner, operational system health badge,
authenticated user badge, and active persona status.
"""
import streamlit as st
import textwrap


def render_header(current_persona: str = "Claims Adjuster (Employee)") -> None:
    """Renders the top enterprise header bar."""
    user_email = st.session_state.get("user_email", "wrenchwise@gmail.com")
    st.markdown(textwrap.dedent(f"""
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
            <span class="status-badge badge-navy" title="Authenticated User">
                🔐 {user_email}
            </span>
            <span class="status-badge badge-blue" title="Active Organization Role">
                👤 {current_persona.split('(')[0].strip()}
            </span>
            <span class="status-badge badge-navy" style="cursor:pointer;" title="Enterprise Configuration">
                ⚙️ Config
            </span>
        </div>
    </div>
    """), unsafe_allow_html=True)
