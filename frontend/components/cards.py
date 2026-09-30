"""
Reusable Card and KPI components for InsurAgent enterprise UI.
"""
import streamlit as st
from typing import Optional
from frontend.styles import render_html


def render_kpi_card(
    title: str,
    value: str,
    description: str,
    status_text: Optional[str] = None,
    status_type: str = "green",
    trend_text: Optional[str] = None,
    trend_positive: bool = True
) -> None:
    """Renders a structured, polished enterprise KPI card."""
    badge_class = f"badge-{status_type}"
    status_badge_html = f'<span class="status-badge {badge_class}">{status_text}</span>' if status_text else ''
    
    trend_html = ""
    if trend_text:
        t_color = "#047857" if trend_positive else "#b91c1c"
        t_arrow = "↑" if trend_positive else "↓"
        trend_html = f'<span style="font-size:11px; font-weight:700; color:{t_color}; margin-left:6px;">{t_arrow} {trend_text}</span>'

    card_html = f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <div class="kpi-title">{title}</div>
            {status_badge_html}
        </div>
        <div>
            <div class="kpi-value">{value}{trend_html}</div>
        </div>
        <div class="kpi-footer">
            <span style="color:#64748b; font-size:11px;">{description}</span>
        </div>
    </div>
    """
    render_html(card_html)


def render_status_badge(text: str, badge_type: str = "blue") -> str:
    """Returns HTML for an enterprise status badge."""
    return f'<span class="status-badge badge-{badge_type}">{text}</span>'
