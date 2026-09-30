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
    Renders the role-based enterprise sidebar navigation for Developer or End User.
    """
    role_type = st.session_state.get("role_type", "claims_adjuster")
    user_role = st.session_state.get("user_role", "Claims Adjuster")
    user_email = st.session_state.get("user_email", "wrenchwise@gmail.com")

    with st.sidebar:
        # Top Brand Header
        if role_type == "developer":
            sidebar_sub = "Technical Operations"
            role_label = "Developer / Technical Operations"
            account_title = "Developer"
        else:
            sidebar_sub = "Enterprise Insurance Claims Intelligence Platform"
            role_label = "Claims Adjuster"
            account_title = "Claims Adjuster"

        header_html = f"""
        <div style="display:flex;align-items:center;gap:10px;padding:4px 0 12px 0;border-bottom:1px solid #1e2e42;margin-bottom:14px;">
            <div style="width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg, #0284c7 0%, #0369a1 100%);display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 2px 6px rgba(2,132,199,0.3);">🛡️</div>
            <div>
                <div style="font-size:16px;font-weight:800;letter-spacing:-0.3px;color:#ffffff;line-height:1.15;">INSURAGENT</div>
                <div class="sidebar-subtitle-text" style="font-size:10px; color:#38bdf8;">{sidebar_sub}</div>
            </div>
        </div>
        """
        render_html(header_html)

        # Authenticated Persona Status Pill
        role_card_html = f"""
        <div style="background:#0f2744; border:1px solid #1e3a5f; border-radius:8px; padding:8px 12px; margin-bottom:14px; display:flex; align-items:center; justify-content:space-between;">
            <div>
                <div style="font-size:9.5px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:0.6px;">Active Persona</div>
                <div style="font-size:12.5px; font-weight:750; color:#ffffff; margin-top:2px;">{role_label}</div>
            </div>
            <span style="font-size:9.5px; font-weight:700; background:#0284c7; color:#ffffff; padding:2px 8px; border-radius:12px;">Active</span>
        </div>
        """
        render_html(role_card_html)
        st.session_state["current_persona"] = role_label

        # Define Navigation items and formatting based on role
        if role_type == "developer":
            dev_tech_items = [
                "Technical Dashboard",
                "Agent Workflow",
                "Knowledge / RAG",
                "MCP Tools",
                "Guardrails",
                "Human-in-the-Loop",
                "Model Evaluation",
                "Cost Analytics",
                "Token Usage",
                "Audit & Traceability",
                "System Health",
                "Execution Logs"
            ]
            dev_biz_items = [
                "Claims",
                "Risk & Fraud"
            ]
            all_nav_items = dev_tech_items + dev_biz_items

            icons_map = {
                "Technical Dashboard": "📊  Technical Dashboard",
                "Agent Workflow": "⚙️  Agent Workflow",
                "Knowledge / RAG": "🧠  Knowledge / RAG",
                "MCP Tools": "🔌  MCP Tools",
                "Guardrails": "🛡️  Guardrails",
                "Human-in-the-Loop": "👤  Human-in-the-Loop",
                "Model Evaluation": "🎯  Model Evaluation",
                "Cost Analytics": "💰  Cost Analytics",
                "Token Usage": "⚡  Token Usage",
                "Audit & Traceability": "🔍  Audit & Traceability",
                "System Health": "❤️  System Health",
                "Execution Logs": "📋  Execution Logs",
                "Claims": "📋  Claims",
                "Risk & Fraud": "🚨  Risk & Fraud"
            }

            curr_page = st.session_state.get("active_nav_page", "Technical Dashboard")
            if curr_page not in all_nav_items:
                curr_page = "Technical Dashboard"

            all_formatted = [icons_map[p] for p in all_nav_items]
            current_fmt = icons_map.get(curr_page, icons_map["Technical Dashboard"])
            default_index = all_formatted.index(current_fmt) if current_fmt in all_formatted else 0

            st.markdown("<div class='sidebar-section-header'>TECHNICAL OVERVIEW</div>", unsafe_allow_html=True)
            selected_fmt = st.radio(
                "Developer Navigation",
                all_formatted,
                index=default_index,
                label_visibility="collapsed",
                key="dev_nav_radio"
            )

            rev_map = {v: k for k, v in icons_map.items()}
            selected_page = rev_map.get(selected_fmt, "Technical Dashboard")
            st.session_state.active_nav_page = selected_page

        else:
            # End User Navigation
            user_main_items = [
                "Dashboard",
                "Claims",
                "AI Assistant",
                "My Claims",
                "Documents"
            ]
            user_support_items = [
                "Knowledge Center",
                "Help & Support"
            ]
            all_nav_items = user_main_items + user_support_items

            icons_map = {
                "Dashboard": "📊  Dashboard",
                "Claims": "📋  Claims",
                "AI Assistant": "💬  AI Assistant",
                "My Claims": "📑  My Claims",
                "Documents": "📎  Documents",
                "Knowledge Center": "📚  Knowledge Center",
                "Help & Support": "❓  Help & Support"
            }

            curr_page = st.session_state.get("active_nav_page", "Dashboard")
            if curr_page not in all_nav_items:
                curr_page = "Dashboard"

            all_formatted = [icons_map[p] for p in all_nav_items]
            current_fmt = icons_map.get(curr_page, icons_map["Dashboard"])
            default_index = all_formatted.index(current_fmt) if current_fmt in all_formatted else 0

            st.markdown("<div class='sidebar-section-header'>MAIN</div>", unsafe_allow_html=True)
            selected_fmt = st.radio(
                "User Navigation",
                all_formatted,
                index=default_index,
                label_visibility="collapsed",
                key="user_nav_radio"
            )

            rev_map = {v: k for k, v in icons_map.items()}
            selected_page = rev_map.get(selected_fmt, "Dashboard")
            st.session_state.active_nav_page = selected_page

        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

        # Bottom Sticky/Fixed Account & Sign Out Section
        st.markdown("<div class='sidebar-section-header' style='margin-top:0;'>ACCOUNT</div>", unsafe_allow_html=True)

        account_html = f"""
        <div class="sidebar-account-box">
            <div style="font-size:12.5px; font-weight:750; color:#ffffff;">{account_title}</div>
            <div style="font-size:11px; color:#38bdf8; word-break:break-all; margin-top:2px;">{user_email}</div>
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
            st.session_state["role_type"] = None
            st.session_state["current_persona"] = None
            st.session_state["active_nav_page"] = "Dashboard"
            st.rerun()

        st.caption("v2.4 Enterprise Production Release")

    return selected_page, role_label


