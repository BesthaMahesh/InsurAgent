"""
Enterprise Login View for InsurAgent Platform.
Provides a secure, high-trust authentication portal matching the enterprise design system.
Supports Role-Based Access for Internal Developers/Administrators and Claims Adjusters.
"""
import streamlit as st
import os
import time
from frontend.styles import render_html

# Authorized Enterprise Accounts
ACCOUNTS = {
    "wrenchwisedevoloper@gmail.com": {
        "password": os.getenv("ADMIN_AUTH_PASSWORD", "123456").strip(),
        "role": "Developer / Technical Operations",
        "role_type": "developer",
        "default_persona": "Developer / Technical Operations",
        "default_page": "Technical Dashboard"
    },
    "wrenchwise@gmail.com": {
        "password": os.getenv("USER_AUTH_PASSWORD", "12345").strip(),
        "role": "Claims Adjuster",
        "role_type": "claims_adjuster",
        "default_persona": "Claims Adjuster",
        "default_page": "Dashboard"
    }
}


def render_login_view() -> None:
    """Renders the enterprise login screen and handles authentication."""
    _, col_main, _ = st.columns([1, 1.8, 1])

    with col_main:
        header_html = """
        <div style="text-align:center; margin-top:2.5rem; margin-bottom:1.5rem;">
            <div style="width:58px; height:58px; border-radius:14px; background:linear-gradient(135deg, #091524 0%, #0f2744 100%); display:inline-flex; align-items:center; justify-content:center; box-shadow:0 8px 20px -4px rgba(2, 132, 199, 0.35); border:1px solid #1e3a5f; margin-bottom:12px;">
                <span style="font-size:26px;">🛡️</span>
            </div>
            <div style="font-size:24px; font-weight:800; color:#0f172a; letter-spacing:-0.5px; line-height:1.2;">INSURAGENT</div>
            <div style="font-size:13px; font-weight:600; color:#0284c7; margin-top:3px;">Enterprise Insurance Claims Intelligence Platform</div>
            <div style="font-size:12px; color:#64748b; margin-top:4px;">Sign in to access your role-based workspace</div>
        </div>
        """
        render_html(header_html)

        # Login Form Card
        with st.container(border=True):
            with st.form("enterprise_login_form", clear_on_submit=False):
                st.markdown("<div style='font-size:12.5px; font-weight:700; color:#334155; margin-bottom:4px;'>Authorized Email Address</div>", unsafe_allow_html=True)
                email_input = st.text_input(
                    "Email",
                    value="",
                    placeholder="Enter your enterprise email address",
                    label_visibility="collapsed"
                )

                st.markdown("<div style='font-size:12.5px; font-weight:700; color:#334155; margin-top:10px; margin-bottom:4px;'>Access Key / Password</div>", unsafe_allow_html=True)
                password_input = st.text_input(
                    "Password",
                    type="password",
                    value="",
                    placeholder="Enter your security key / password",
                    label_visibility="collapsed"
                )

                st.write("")
                submit_button = st.form_submit_button(
                    "Sign In",
                    use_container_width=True,
                    type="primary"
                )

                if submit_button:
                    entered_email = email_input.strip().lower()
                    entered_password = password_input.strip()

                    if entered_email in ACCOUNTS and entered_password == ACCOUNTS[entered_email]["password"]:
                        account_info = ACCOUNTS[entered_email]
                        st.session_state["authenticated"] = True
                        st.session_state["user_email"] = entered_email
                        st.session_state["user_role"] = account_info["role"]
                        st.session_state["role_type"] = account_info["role_type"]
                        st.session_state["current_persona"] = account_info["default_persona"]
                        st.session_state["active_nav_page"] = account_info["default_page"]
                        st.toast(f"Authenticated as {account_info['role']}. Welcome to InsurAgent!", icon="🛡️")
                        time.sleep(0.3)
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please verify your authorized email address and password.")

        footer_html = """
        <div style="text-align:center; margin-top:20px; font-size:11.5px; color:#94a3b8; line-height:1.6;">
            🛡️ <b>InsurAgent Enterprise Security Layer</b> &bull; SOC 2 Type II Certified<br>
            Multi-agent adjudication trails and decisions are cryptographically signed &amp; timestamped.
        </div>
        """
        render_html(footer_html)

