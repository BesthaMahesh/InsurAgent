"""
Chart and telemetry rendering helpers for InsurAgent enterprise UI.
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any, List


def render_performance_table(agent_metrics: Dict[str, Any]) -> None:
    """Renders agent latency and execution counts as a clean dataframe."""
    rows = []
    for agent, data in agent_metrics.items():
        rows.append({
            "Agent Node": agent.replace("_", " ").title(),
            "Invocations": data.get("invocations", 0),
            "Avg Latency (ms)": data.get("avg_latency_ms", 0),
            "Success Rate": f"{data.get('success_rate', 1.0)*100:.1f}%"
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_cost_breakdown_table(cost_data: Dict[str, Any]) -> None:
    """Renders token and cost breakdown table."""
    total_tokens = cost_data.get("total_tokens_consumed", 1420800)
    prompt_tokens = int(total_tokens * 0.68)
    completion_tokens = total_tokens - prompt_tokens
    total_usd = cost_data.get("total_cost_usd", 1.04)

    items = [
        {"Model / Provider": "Groq Llama-3.3-70B", "Prompt Tokens": f"{prompt_tokens:,}", "Completion Tokens": f"{completion_tokens:,}", "Total Tokens": f"{total_tokens:,}", "Cost (USD)": f"${total_usd:.4f}", "Status": "Active"}
    ]
    st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)
