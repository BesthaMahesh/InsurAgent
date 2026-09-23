"""
Agent Status and Execution Card components for InsurAgent enterprise UI.
"""
import streamlit as st
import textwrap
from typing import Dict, Any, Optional


def render_agent_card(
    agent_name: str,
    purpose: str,
    status: str = "Completed",
    execution_time_ms: int = 145,
    tools_used: Optional[str] = "None",
    input_desc: Optional[str] = None,
    output_desc: Optional[str] = None,
    confidence: Optional[float] = None
) -> None:
    """Renders a single specialized agent card with execution details."""
    status_cls = "badge-green" if status == "Completed" or status == "Healthy" else "badge-amber"
    conf_str = f" • Conf: {confidence*100:.0f}%" if confidence is not None else ""

    st.markdown(textwrap.dedent(f"""
    <div class="agent-card">
        <div class="agent-card-header">
            <div>
                <span class="agent-card-title">{agent_name}</span>
                <span style="font-size:11px; color:#64748b; margin-left:6px;">{purpose}</span>
            </div>
            <div style="display:flex; gap:6px;">
                <span class="status-badge {status_cls}">● {status}</span>
                <span class="status-badge badge-navy">{execution_time_ms} ms{conf_str}</span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; font-size:11.5px; background:#f8fafc; padding:8px 10px; border-radius:6px; margin-top:8px;">
            <div>
                <span style="color:#64748b; font-weight:600;">Input:</span> {input_desc or 'Normalized State Payload'}
            </div>
            <div>
                <span style="color:#64748b; font-weight:600;">Output:</span> {output_desc or 'Structured Decision Context'}
            </div>
        </div>
        <div style="font-size:10.5px; color:#64748b; margin-top:6px;">
            <b>Tools / Knowledge Integrations:</b> <code>{tools_used}</code>
        </div>
    </div>
    """), unsafe_allow_html=True)
