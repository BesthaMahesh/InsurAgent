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
    Maintains the original visual design and layout for End Users while providing
    a dedicated technical navigation for Developers.
    """
    # Enforce role type strictly from authenticated user email
    user_email = (st.session_state.get("user_email") or "wrenchwise@gmail.com").strip().lower()
    if user_email in ("wrenchwisedevoloper@gmail.com", "wrenchwisedeveloper@gmail.com"):
        role_type = "developer"
        user_role = "Developer / Technical Operations"
        sidebar_sub = "Technical Operations"
        default_home_page = "Technical Dashboard"
    else:
        role_type = "claims_adjuster"
        user_role = "Claims Adjuster"
        sidebar_sub = "Claims Intelligence Platform"
        default_home_page = "Dashboard"

    st.session_state["role_type"] = role_type
    st.session_state["user_role"] = user_role

    with st.sidebar:
        # Top Brand Header (Original InsurAgent Header Placement & Styling)
        header_html = f"""
        <div style="display:flex;align-items:center;gap:10px;padding:4px 0 14px 0;border-bottom:1px solid #1e2e42;margin-bottom:12px;">
            <div style="width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg, #0284c7 0%, #0369a1 100%);display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 2px 6px rgba(2,132,199,0.3);">🛡️</div>
            <div>
                <div style="font-size:16px;font-weight:800;letter-spacing:-0.3px;color:#ffffff;line-height:1.15;">INSURAGENT</div>
                <div class="sidebar-subtitle-text" style="font-size:10px; color:#38bdf8; font-weight:600; letter-spacing:0.2px; margin-top:2px;">{sidebar_sub}</div>
            </div>
        </div>
        """
        render_html(header_html)

        # -----------------------------------------------------------------
        # END USER SIDEBAR (Original Visual Design & Structure)
        # -----------------------------------------------------------------
        if role_type != "developer":
            # 1. USER / PERSONA Section (Original Dropdown Selector)
            st.markdown("<div class='sidebar-section-header' style='margin-top:0;'>USER / PERSONA</div>", unsafe_allow_html=True)
            persona_options = [
                "Claims Adjuster (Employee)",
                "Senior Underwriter",
                "Fraud Investigator (SIU)",
                "Compliance & Audit Officer"
            ]
            saved_persona = st.session_state.get("current_persona", "Claims Adjuster (Employee)")
            persona_idx = persona_options.index(saved_persona) if saved_persona in persona_options else 0
            
            selected_persona = st.selectbox(
                "",
                persona_options,
                index=persona_idx,
                label_visibility="collapsed",
                key="end_user_persona_select"
            )
            st.session_state["current_persona"] = selected_persona
            persona = selected_persona

            # 2. NAVIGATION Section (Original Header & Clean Radio Menu)
            st.markdown("<div class='sidebar-section-header'>NAVIGATION</div>", unsafe_allow_html=True)

            user_nav_items = [
                "Dashboard",
                "Claims",
                "AI Assistant",
                "My Claims",
                "Documents",
                "Knowledge Center",
                "Help & Support"
            ]

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
            if curr_page not in user_nav_items:
                curr_page = "Dashboard"
                st.session_state["active_nav_page"] = "Dashboard"

            all_formatted = [icons_map[p] for p in user_nav_items]
            current_fmt = icons_map.get(curr_page, icons_map["Dashboard"])

            if "main_user_nav_radio" not in st.session_state or st.session_state["main_user_nav_radio"] not in all_formatted:
                st.session_state["main_user_nav_radio"] = current_fmt

            def _on_user_nav_change():
                sel = st.session_state.get("main_user_nav_radio")
                if sel in rev_map:
                    st.session_state["active_nav_page"] = rev_map[sel]

            rev_map = {v: k for k, v in icons_map.items()}

            selected_fmt = st.radio(
                "",
                all_formatted,
                key="main_user_nav_radio",
                on_change=_on_user_nav_change,
                label_visibility="collapsed"
            )

            selected_page = rev_map.get(selected_fmt, "Dashboard")
            st.session_state["active_nav_page"] = selected_page

            st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

            # 3. ACCOUNT Section (Original Enterprise Box & Clean Sign Out)
            st.markdown("<div class='sidebar-section-header' style='margin-top:0;'>ACCOUNT</div>", unsafe_allow_html=True)
            account_html = f"""
            <div class="sidebar-account-box">
                <div style="font-size:12px; font-weight:750; color:#ffffff;">Claims Adjuster</div>
                <div style="font-size:11px; font-weight:600; color:#38bdf8; word-break:break-all; margin-top:2px;">{user_email}</div>
                <div style="font-size:10px; color:#10b981; font-weight:600; margin-top:4px; display:flex; align-items:center; gap:4px;">
                    <span>●</span> Authorized Session
                </div>
            </div>
            """
            render_html(account_html)

            st.markdown("<div class='sidebar-logout-wrapper'>", unsafe_allow_html=True)
            if st.button("🚪 Sign Out", key="sidebar_logout_btn", use_container_width=True):
                st.session_state.clear()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            st.caption("v2.4 Enterprise Production Release")

        # -----------------------------------------------------------------
        # DEVELOPER SIDEBAR (Technical Operations Navigation)
        # -----------------------------------------------------------------
        else:
            # 1. USER / PERSONA Section
            st.markdown("<div class='sidebar-section-header' style='margin-top:0;'>USER / PERSONA</div>", unsafe_allow_html=True)
            dev_personas = [
                "Developer / Technical Operations",
                "System Architect",
                "MLOps / LLM Evaluator"
            ]
            saved_persona = st.session_state.get("current_persona", "Developer / Technical Operations")
            dev_idx = dev_personas.index(saved_persona) if saved_persona in dev_personas else 0

            selected_persona = st.selectbox(
                "",
                dev_personas,
                index=dev_idx,
                label_visibility="collapsed",
                key="dev_persona_select"
            )
            st.session_state["current_persona"] = selected_persona
            persona = selected_persona

            # 2. SECTIONS FOR DEVELOPER HIERARCHY
            dev_sections = [
                (
                    "TECHNICAL OVERVIEW",
                    [
                        ("Technical Dashboard", "▣  Technical Dashboard"),
                        ("Agent Workflow", "⚙️  Agent Workflow"),
                        ("Knowledge / RAG", "🧠  Knowledge / RAG"),
                        ("MCP Tools", "🔌  MCP Tools"),
                        ("Guardrails", "🛡️  Guardrails")
                    ]
                ),
                (
                    "AI GOVERNANCE",
                    [
                        ("Human-in-the-Loop", "👤  Human-in-the-Loop"),
                        ("Model Evaluation", "📊  Model Evaluation"),
                        ("Audit & Traceability", "🔍  Audit & Traceability")
                    ]
                ),
                (
                    "AI OPERATIONS",
                    [
                        ("Cost Analytics", "💰  Cost Analytics"),
                        ("Token Usage", "⚡  Token Usage"),
                        ("System Health", "❤️  System Health"),
                        ("Execution Logs", "📋  Execution Logs")
                    ]
                ),
                (
                    "BUSINESS OPERATIONS",
                    [
                        ("Claims", "📄  Claims"),
                        ("Risk & Fraud", "🚨  Risk & Fraud")
                    ]
                )
            ]

            valid_pages = [page for _, items in dev_sections for page, _ in items]
            curr_page = st.session_state.get("active_nav_page", default_home_page)
            if curr_page not in valid_pages:
                curr_page = default_home_page
                st.session_state["active_nav_page"] = default_home_page

            for sec_title, sec_items in dev_sections:
                st.markdown(f"<div class='sidebar-section-header'>{sec_title}</div>", unsafe_allow_html=True)
                for page_name, label_text in sec_items:
                    is_active = (curr_page == page_name)
                    btn_text = f"{'● ' if is_active else '  '}{label_text}"
                    btn_key = f"dev_nav_btn_{page_name.replace(' ', '_').replace('/', '_')}"
                    if st.button(btn_text, key=btn_key, type="primary" if is_active else "secondary", use_container_width=True):
                        st.session_state["active_nav_page"] = page_name
                        st.rerun()

            selected_page = st.session_state.get("active_nav_page", default_home_page)

            st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

            # 3. ACCOUNT Section
            st.markdown("<div class='sidebar-section-header' style='margin-top:0;'>ACCOUNT</div>", unsafe_allow_html=True)
            account_html = f"""
            <div class="sidebar-account-box">
                <div style="font-size:12px; font-weight:750; color:#ffffff;">Developer</div>
                <div style="font-size:11px; font-weight:600; color:#38bdf8; word-break:break-all; margin-top:2px;">{user_email}</div>
                <div style="font-size:10px; color:#10b981; font-weight:600; margin-top:4px; display:flex; align-items:center; gap:4px;">
                    <span>●</span> Authorized Session
                </div>
            </div>
            """
            render_html(account_html)

            st.markdown("<div class='sidebar-logout-wrapper'>", unsafe_allow_html=True)
            if st.button("🚪 Sign Out", key="dev_sidebar_logout_btn", use_container_width=True):
                st.session_state.clear()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            st.caption("v2.4 Enterprise Production Release")

    return selected_page, persona
