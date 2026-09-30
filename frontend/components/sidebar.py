"""
Sidebar component for InsurAgent enterprise navigation.
Implements the 13-item client-facing information architecture,
clear section separation, role status, and sticky Sign Out.
"""
import streamlit as st
from typing import Tuple
from frontend.styles import render_html


def render_sidebar() -> Tuple[str, str]:
    """
    Renders the enterprise sidebar navigation and returns selected page and active persona.
    """
    with st.sidebar:
        # Top Brand Header
        header_html = """
        <div style="display:flex;align-items:center;gap:10px;padding:4px 0 12px 0;border-bottom:1px solid #1e2e42;margin-bottom:12px;">
            <div style="width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg, #0284c7 0%, #0369a1 100%);display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 2px 6px rgba(2,132,199,0.3);">🛡️</div>
            <div>
                <div style="font-size:16px;font-weight:800;letter-spacing:-0.3px;color:#ffffff;line-height:1.15;">INSURAGENT</div>
                <div class="sidebar-subtitle-text">Claims Intelligence Platform</div>
            </div>
        </div>
        """
        render_html(header_html)

        # User / Persona Switcher
        st.markdown("<div class='sidebar-section-header' style='margin-top:0;'>USER / PERSONA</div>", unsafe_allow_html=True)
        default_persona = st.session_state.get("current_persona", "Claims Adjuster (Employee)")
        persona_options = [
            "Claims Adjuster (Employee)",
            "Internal Administrator (Admin)",
            "Claimant / Policyholder",
            "Hospital / Garage Partner",
            "Senior Claim Auditor",
            "Compliance Officer"
        ]
        default_idx = persona_options.index(default_persona) if default_persona in persona_options else 0
        persona = st.selectbox(
            "Persona",
            persona_options,
            index=default_idx,
            label_visibility="collapsed"
        )
        st.session_state["current_persona"] = persona

        # Navigation Options (13 items)
        nav_items = [
            "Dashboard",
            "Claims",
            "Model Evaluation",
            "Cost Analysis",
            "AI Assistant",
            "Usage & Tokens",
            # Operations & Controls
            "Processing Workflow",
            "Knowledge Center",
            "Risk & Fraud",
            "Human Review",
            "Audit & Compliance",
            "Trust & Responsible AI",
            "System Health"
        ]

        # Check current active page
        curr_page = st.session_state.get("active_nav_page", "Dashboard")
        if curr_page not in nav_items:
            curr_page = "Dashboard"

        icons_map = {
            "Dashboard": "📊  Dashboard",
            "Claims": "📋  Claims",
            "Model Evaluation": "🎯  Model Evaluation",
            "Cost Analysis": "💳  Cost Analysis",
            "AI Assistant": "💬  AI Assistant",
            "Usage & Tokens": "⚡  Usage & Tokens",
            "Processing Workflow": "🔄  Processing Workflow",
            "Knowledge Center": "📚  Knowledge Center",
            "Risk & Fraud": "🚨  Risk & Fraud",
            "Human Review": "⚖️  Human Review",
            "Audit & Compliance": "🔒  Audit & Compliance",
            "Trust & Responsible AI": "🛡️  Trust & Responsible AI",
            "System Health": "🩺  System Health"
        }

        all_formatted = [icons_map[p] for p in nav_items]
        current_fmt = icons_map.get(curr_page, icons_map["Dashboard"])
        default_index = all_formatted.index(current_fmt) if current_fmt in all_formatted else 0

        st.markdown("<div class='sidebar-section-header'>MAIN NAVIGATION</div>", unsafe_allow_html=True)

        selected_fmt = st.radio(
            "Navigation Menu",
            all_formatted,
            index=default_index,
            label_visibility="collapsed",
            key="main_nav_radio"
        )

        rev_map = {v: k for k, v in icons_map.items()}
        selected_page = rev_map.get(selected_fmt, "Dashboard")
        st.session_state.active_nav_page = selected_page

        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

        # Bottom Sticky/Fixed Account & Sign Out Section
        user_email = st.session_state.get("user_email", "wrenchwise@gmail.com")
        user_role = st.session_state.get("user_role", "Claims Adjuster")

        account_html = f"""
        <div class="sidebar-account-box">
            <div style="font-size:9.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:0.6px;">Active Account</div>
            <div style="font-size:12.5px; font-weight:700; color:#ffffff; margin-top:2px;">{user_role}</div>
            <div style="font-size:11px; color:#38bdf8; word-break:break-all; margin-top:1px;">{user_email}</div>
            <div style="font-size:10px; color:#10b981; font-weight:600; margin-top:4px; display:flex; align-items:center; gap:4px;">
                <span>●</span> Authorized Session
            </div>
        </div>
        """
        render_html(account_html)

        if st.button("🚪 Sign Out", key="sidebar_logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["user_email"] = None
            st.session_state["user_role"] = None
            st.session_state["active_nav_page"] = "Dashboard"
            st.rerun()

        st.caption("v2.4 Enterprise Production Release")

    return selected_page, persona
