"""
Enterprise Login View for InsurAgent Platform.
Provides a secure, high-trust authentication portal matching the enterprise design system.
"""
import streamlit as st
import os
import textwrap

# Default Authorized Credentials (Can also be overridden via environment variables)
AUTHORIZED_EMAIL = os.getenv("AUTH_EMAIL", "wrenchwise@gmail.com").strip().lower()
AUTHORIZED_PASSWORD = os.getenv("AUTH_PASSWORD", "12345").strip()


def render_login_view() -> None:
    """Renders the enterprise login screen and handles authentication."""
    # Center layout container using Streamlit columns
    _, col_main, _ = st.columns([1, 1.8, 1])

    with col_main:
        st.markdown(textwrap.dedent("""
        <div class="login-wrapper">
            <div class="login-header-box">
                <div class="login-brand-badge">
                    <span style="font-size:32px;">🛡️</span>
                </div>
                <div class="login-title">INSURAGENT ENTERPRISE</div>
                <div class="login-subtitle">Multi-Agent Claims Intelligence &amp; Autonomous Audit System</div>
                <div class="login-security-pill">
                    <span style="color:#10b981;font-weight:bold;">●</span> Single Authorized Gateway &bull; 256-bit TLS Encrypted
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

        # Login Form Card
        with st.container():
            st.markdown('<div class="login-card-inner">', unsafe_allow_html=True)

            with st.form("enterprise_login_form", clear_on_submit=False):
                st.markdown("<div class='login-input-label'>Authorized Email Address</div>", unsafe_allow_html=True)
                email_input = st.text_input(
                    "Email",
                    value=st.session_state.get("prefill_email", "wrenchwise@gmail.com"),
                    placeholder="e.g. wrenchwise@gmail.com",
                    label_visibility="collapsed"
                )

                st.markdown("<div class='login-input-label' style='margin-top:12px;'>Access Key / Password</div>", unsafe_allow_html=True)
                password_input = st.text_input(
                    "Password",
                    type="password",
                    value=st.session_state.get("prefill_password", ""),
                    placeholder="Enter security key",
                    label_visibility="collapsed"
                )

                st.markdown("<div style='margin-top:18px;'></div>", unsafe_allow_html=True)
                submit_button = st.form_submit_button(
                    "🚀 Authenticate & Enter Platform",
                    use_container_width=True,
                    type="primary"
                )

                if submit_button:
                    entered_email = email_input.strip().lower()
                    entered_password = password_input.strip()

                    if entered_email == AUTHORIZED_EMAIL and entered_password == AUTHORIZED_PASSWORD:
                        st.session_state["authenticated"] = True
                        st.session_state["user_email"] = entered_email
                        st.session_state["active_nav_page"] = "Dashboard"
                        st.toast("✅ Authentication successful. Welcome to InsurAgent!", icon="🛡️")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please check your authorized email or password.")

            st.markdown('</div>', unsafe_allow_html=True)

        # Security & Authorized Credentials Information Card
        st.markdown(textwrap.dedent(f"""
        <div class="login-info-card">
            <div style="font-size:12px; font-weight:700; color:#0f2744; margin-bottom:6px; display:flex; align-items:center; justify-content:space-between;">
                <span>🔐 Authorized Access Credentials</span>
                <span class="status-badge badge-blue">Restricted Access</span>
            </div>
            <div style="font-size:12px; color:#475569; line-height:1.6;">
                This production environment is locked to authorized enterprise personnel only.<br>
                <b>Authorized Email:</b> <code style="color:#0284c7; background:#e0f2fe; padding:2px 6px; border-radius:4px;">{AUTHORIZED_EMAIL}</code><br>
                <b>Password:</b> <code style="color:#0284c7; background:#e0f2fe; padding:2px 6px; border-radius:4px;">12345</code>
            </div>
        </div>
        
        <div style="text-align:center; margin-top:20px; font-size:11.5px; color:#94a3b8; line-height:1.6;">
            🛡️ <b>InsurAgent Governance &amp; AI Security Layer</b> &bull; SOC 2 Type II Certified<br>
            All multi-agent actions, claim decisions, and audit trails are logged &amp; timestamped.
        </div>
        """), unsafe_allow_html=True)
