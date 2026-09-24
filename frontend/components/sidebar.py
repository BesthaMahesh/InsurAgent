"""
Sidebar component for InsurAgent enterprise navigation.
"""
import streamlit as st
import textwrap
from typing import Tuple


def render_sidebar() -> Tuple[str, str]:
    """
    Renders the sidebar navigation and returns selected page and active persona.
    """
    with st.sidebar:
        st.markdown(textwrap.dedent("""
        <div style="display:flex;align-items:center;gap:10px;padding:6px 0 12px 0;">
            <div style="width:34px;height:34px;border-radius:8px;background:#0284c7;display:flex;align-items:center;justify-content:center;font-size:18px;">🛡️</div>
            <div>
                <div style="font-size:16px;font-weight:800;letter-spacing:-0.3px;color:#ffffff;">InsurAgent</div>
                <div style="font-size:10px;color:#94a3b8;">Claims Intelligence Platform</div>
            </div>
        </div>
        """), unsafe_allow_html=True)

        st.markdown("<div style='font-size:11px;font-weight:700;color:#94a3b8;margin-bottom:4px;'>USER / PERSONA</div>", unsafe_allow_html=True)
        persona = st.selectbox(
            "Persona",
            [
                "Claims Adjuster (Employee)",
                "Claimant / Policyholder",
                "Hospital / Garage Partner",
                "Senior Claim Auditor",
                "Compliance Officer"
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("<div style='margin-top:14px;font-size:11px;font-weight:700;color:#94a3b8;margin-bottom:4px;'>NAVIGATION</div>", unsafe_allow_html=True)
        
        pages = [
            "Dashboard",
            "Claims",
            "AI Assistant",
            "Multi-Agent Workflow",
            "Knowledge / RAG",
            "Risk & Fraud",
            "Human Review",
            "Audit & Traceability",
            "Governance & Responsible AI",
            "Model Evaluation",
            "Cost & Usage",
            "System Monitoring"
        ]

        # Use index from session_state if previously selected
        curr_page = st.session_state.get("active_nav_page", "Dashboard")
        default_index = pages.index(curr_page) if curr_page in pages else 0

        selected_page = st.radio(
            "Navigation Menu",
            pages,
            index=default_index,
            label_visibility="collapsed"
        )
        st.session_state.active_nav_page = selected_page

        # Logged-in user information & Sign Out
        user_email = st.session_state.get("user_email", "Enterprise User")
        st.markdown(textwrap.dedent(f"""
        <div style="background:#0f2744; border:1px solid #1e3a5f; border-radius:8px; padding:10px 12px; margin-bottom:12px;">
            <div style="font-size:10px; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:0.5px;">Active Account</div>
            <div style="font-size:12px; font-weight:600; color:#38bdf8; word-break:break-all; margin-top:2px;">{user_email}</div>
            <div style="font-size:10px; color:#10b981; margin-top:4px;">● Authorized Session</div>
        </div>
        """), unsafe_allow_html=True)

        if st.button("🚪 Sign Out", key="sidebar_logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["user_email"] = None
            st.rerun()

        st.divider()

        # Enterprise System Status Panel at Sidebar Bottom
        st.markdown(textwrap.dedent("""
        <div style="font-size:11px; color:#94a3b8; line-height:1.7;">
            <div style="font-weight:700; color:#e2e8f0; margin-bottom:4px;">SYSTEM STATUS</div>
            <div>● <b>API:</b> <span style="color:#10b981;">Connected</span></div>
            <div>● <b>LangGraph:</b> <span style="color:#10b981;">Operational</span></div>
            <div>● <b>RAG:</b> <span style="color:#10b981;">Connected</span></div>
            <div>● <b>MCP:</b> <span style="color:#10b981;">Connected (4 Services)</span></div>
        </div>
        """), unsafe_allow_html=True)

        st.caption("v2.4 Enterprise Release")

    return selected_page, persona

