"""
Header component for InsurAgent enterprise UI.
"""
import streamlit as st
import textwrap


def render_header(current_persona: str = "Claims Adjuster") -> None:
    """Renders the top enterprise header bar."""
    user_email = st.session_state.get("user_email", "wrenchwise@gmail.com")
    st.markdown(textwrap.dedent(f"""
    <div class="top-header-bar">
        <div class="header-brand">
            <div class="header-logo-icon">🛡️</div>
            <div>
                <div class="header-title-text">INSURAGENT</div>
                <div class="header-subtitle-text">Enterprise Multi-Agent Claims Intelligence &amp; Audit Platform</div>
            </div>
        </div>
        <div class="header-right-meta">
            <span class="status-badge badge-green">● System Status: Operational</span>
            <span class="status-badge badge-navy">🔐 {user_email}</span>
            <span class="status-badge badge-blue">👤 {current_persona}</span>
            <span class="status-badge badge-navy" style="cursor:pointer;" title="Enterprise Settings">⚙️ Config</span>
        </div>
    </div>
    """), unsafe_allow_html=True)

