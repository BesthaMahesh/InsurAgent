"""
Reusable Card and KPI components for InsurAgent enterprise UI.
"""
import streamlit as st
import textwrap
from typing import Optional


def render_kpi_card(
    title: str,
    value: str,
    description: str,
    status_text: Optional[str] = None,
    status_type: str = "green",
    is_demo: bool = False
) -> None:
    """Renders a structured enterprise KPI card."""
    badge_class = f"badge-{status_type}"
    demo_tag = '<span style="font-size:9.5px;color:#94a3b8;font-style:italic;"> (Demo Data)</span>' if is_demo else ''
    status_badge_html = f'<span class="status-badge {badge_class}">{status_text}</span>' if status_text else ''

    st.markdown(textwrap.dedent(f"""
    <div class="kpi-card">
        <div>
            <div class="kpi-title">{title}{demo_tag}</div>
            <div class="kpi-value">{value}</div>
        </div>
        <div class="kpi-footer">
            <span style="color:#64748b; font-size:11px;">{description}</span>
            {status_badge_html}
        </div>
    </div>
    """), unsafe_allow_html=True)


def render_status_badge(text: str, badge_type: str = "blue") -> str:
    """Returns HTML for an enterprise status badge."""
    return f'<span class="status-badge badge-{badge_type}">{text}</span>'
