"""
Chart and telemetry rendering helpers for InsurAgent enterprise UI.
Uses Altair to generate responsive, high-fidelity corporate data visualizations.
"""
import streamlit as st
import pandas as pd
import altair as alt
from typing import Dict, Any, List


# Enterprise Color Palette Constants
COLOR_BLUE = "#0284c7"
COLOR_NAVY = "#0f2744"
COLOR_GREEN = "#10b981"
COLOR_AMBER = "#f59e0b"
COLOR_RED = "#ef4444"
COLOR_PURPLE = "#8b5cf6"
COLOR_SLATE = "#64748b"


def render_claims_trend_chart() -> None:
    """Renders a line/area chart of claims processed over recent days."""
    data = pd.DataFrame({
        "Date": ["Sep 14", "Sep 15", "Sep 16", "Sep 17", "Sep 18", "Sep 19", "Sep 20", "Sep 21", "Sep 22", "Sep 23"],
        "Claims": [64, 78, 82, 95, 104, 88, 92, 110, 125, 125]
    })

    base = alt.Chart(data).encode(
        x=alt.X("Date:N", title=None, axis=alt.Axis(labelAngle=0, labelColor="#64748b", tickColor="#e2e8f0")),
        y=alt.Y("Claims:Q", title="Claims Processed", axis=alt.Axis(labelColor="#64748b", gridColor="#f1f5f9"))
    )

    area = base.mark_area(
        color=alt.Gradient(
            gradient="linear",
            stops=[alt.GradientStop(color="rgba(2,132,199,0.35)", offset=0),
                   alt.GradientStop(color="rgba(2,132,199,0.02)", offset=1)],
            x1=1, x2=1, y1=1, y2=0
        )
    )

    line = base.mark_line(color=COLOR_BLUE, strokeWidth=3)
    points = base.mark_point(color=COLOR_BLUE, size=50, filled=True)

    chart = (area + line + points).properties(
        height=220,
        title=alt.TitleParams(text="Claims Adjudication Trend (Last 10 Days)", fontSize=13, fontWeight="bold", color="#0f172a")
    ).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True)


def render_claims_status_distribution() -> None:
    """Renders a donut chart of claim status distribution."""
    data = pd.DataFrame({
        "Status": ["Completed (Auto)", "In Review (HITL)", "Escalated (SIU)"],
        "Count": [845, 12, 6],
        "Color": [COLOR_GREEN, COLOR_AMBER, COLOR_RED]
    })

    chart = alt.Chart(data).mark_arc(innerRadius=55, stroke="#ffffff", strokeWidth=2).encode(
        theta=alt.Theta("Count:Q"),
        color=alt.Color("Status:N", scale=alt.Scale(domain=data["Status"].tolist(), range=[COLOR_GREEN, COLOR_AMBER, COLOR_RED]),
                        legend=alt.Legend(orient="bottom", labelColor="#475569", title=None)),
        tooltip=["Status", "Count"]
    ).properties(
        height=220,
        title=alt.TitleParams(text="Claims Status Distribution", fontSize=13, fontWeight="bold", color="#0f172a")
    ).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True)


def render_risk_distribution_chart() -> None:
    """Renders a distribution chart of claim risk tiers."""
    data = pd.DataFrame({
        "Risk Tier": ["Low Risk (0.0 - 0.3)", "Medium Risk (0.3 - 0.6)", "High Risk (> 0.6)"],
        "Count": [810, 41, 12],
        "Color": [COLOR_GREEN, COLOR_AMBER, COLOR_RED]
    })

    chart = alt.Chart(data).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X("Risk Tier:N", title=None, axis=alt.Axis(labelAngle=0, labelColor="#64748b")),
        y=alt.Y("Count:Q", title="Claims", axis=alt.Axis(labelColor="#64748b", gridColor="#f1f5f9")),
        color=alt.Color("Risk Tier:N", scale=alt.Scale(domain=data["Risk Tier"].tolist(), range=[COLOR_GREEN, COLOR_AMBER, COLOR_RED]), legend=None),
        tooltip=["Risk Tier", "Count"]
    ).properties(
        height=220,
        title=alt.TitleParams(text="Risk & Anomaly Distribution", fontSize=13, fontWeight="bold", color="#0f172a")
    ).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True)


def render_ai_vs_human_chart() -> None:
    """Renders a donut chart comparing AI auto-adjudication vs human review."""
    data = pd.DataFrame({
        "Processing Channel": ["AI Straight-Through (97.9%)", "Human Adjuster Escalation (2.1%)"],
        "Percentage": [97.9, 2.1]
    })

    chart = alt.Chart(data).mark_arc(innerRadius=55, stroke="#ffffff", strokeWidth=2).encode(
        theta=alt.Theta("Percentage:Q"),
        color=alt.Color("Processing Channel:N", scale=alt.Scale(domain=data["Processing Channel"].tolist(), range=[COLOR_BLUE, COLOR_NAVY]),
                        legend=alt.Legend(orient="bottom", labelColor="#475569", title=None)),
        tooltip=["Processing Channel", alt.Tooltip("Percentage:Q", format=".1f")]
    ).properties(
        height=220,
        title=alt.TitleParams(text="AI vs Human Decision Ratio", fontSize=13, fontWeight="bold", color="#0f172a")
    ).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True)


def render_agent_latency_chart() -> None:
    """Renders a horizontal bar chart of latency per agent node."""
    data = pd.DataFrame({
        "Agent": [
            "1. Claim Intake",
            "2. Doc Intelligence",
            "3. Policy RAG",
            "4. Fraud / Risk",
            "5. Assessment",
            "6. Audit Seal"
        ],
        "Latency_ms": [180, 420, 680, 310, 550, 120]
    })

    chart = alt.Chart(data).mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4, color=COLOR_BLUE).encode(
        y=alt.Y("Agent:N", title=None, sort=None, axis=alt.Axis(labelColor="#475569")),
        x=alt.X("Latency_ms:Q", title="Latency (ms)", axis=alt.Axis(labelColor="#64748b", gridColor="#f1f5f9")),
        tooltip=["Agent", alt.Tooltip("Latency_ms:Q", title="Avg Latency (ms)")]
    ).properties(
        height=220,
        title=alt.TitleParams(text="Processing Latency by Agent Node", fontSize=13, fontWeight="bold", color="#0f172a")
    ).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True)


def render_token_trend_chart() -> None:
    """Renders daily token consumption chart."""
    data = pd.DataFrame({
        "Date": ["Sep 17", "Sep 18", "Sep 19", "Sep 20", "Sep 21", "Sep 22", "Sep 23"],
        "Input Tokens": [98000, 115000, 128000, 142000, 155000, 168000, 175000],
        "Output Tokens": [42000, 49000, 56000, 61000, 68000, 72000, 76000]
    })
    melted = data.melt(id_vars=["Date"], var_name="Type", value_name="Tokens")

    chart = alt.Chart(melted).mark_bar().encode(
        x=alt.X("Date:N", title=None, axis=alt.Axis(labelAngle=0, labelColor="#64748b")),
        y=alt.Y("Tokens:Q", title="Tokens Consumed", axis=alt.Axis(labelColor="#64748b", gridColor="#f1f5f9")),
        color=alt.Color("Type:N", scale=alt.Scale(domain=["Input Tokens", "Output Tokens"], range=[COLOR_BLUE, COLOR_PURPLE]),
                        legend=alt.Legend(orient="top", labelColor="#475569", title=None)),
        tooltip=["Date", "Type", alt.Tooltip("Tokens:Q", format=",")]
    ).properties(
        height=240,
        title=alt.TitleParams(text="Daily Token Usage Breakdown", fontSize=13, fontWeight="bold", color="#0f172a")
    ).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True)


def render_token_agent_breakdown_chart() -> None:
    """Renders token usage per agent node."""
    data = pd.DataFrame({
        "Agent Node": [
            "Policy Verification",
            "Claim Assessment",
            "Document Analysis",
            "Risk & Fraud",
            "Claim Intake",
            "Audit & Compliance"
        ],
        "Avg Tokens / Claim": [1130, 870, 720, 580, 405, 465]
    })

    chart = alt.Chart(data).mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4, color=COLOR_PURPLE).encode(
        y=alt.Y("Agent Node:N", title=None, sort="-x", axis=alt.Axis(labelColor="#475569")),
        x=alt.X("Avg Tokens / Claim:Q", title="Average Tokens Consumed", axis=alt.Axis(labelColor="#64748b", gridColor="#f1f5f9")),
        tooltip=["Agent Node", "Avg Tokens / Claim"]
    ).properties(
        height=240,
        title=alt.TitleParams(text="Token Consumption by Agent Node", fontSize=13, fontWeight="bold", color="#0f172a")
    ).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True)


def render_cost_by_agent_chart() -> None:
    """Renders cost by agent bar chart."""
    data = pd.DataFrame({
        "Agent Node": [
            "Policy Verification",
            "Claim Assessment",
            "Document Analysis",
            "Claim Intake",
            "Risk & Fraud",
            "Audit & Compliance"
        ],
        "Cost_USD": [0.00072, 0.00056, 0.00046, 0.00026, 0.00037, 0.00030]
    })

    chart = alt.Chart(data).mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4, color=COLOR_GREEN).encode(
        y=alt.Y("Agent Node:N", title=None, sort="-x", axis=alt.Axis(labelColor="#475569")),
        x=alt.X("Cost_USD:Q", title="Cost per Adjudication (USD)", axis=alt.Axis(labelColor="#64748b", gridColor="#f1f5f9", format="$.5f")),
        tooltip=["Agent Node", alt.Tooltip("Cost_USD:Q", format="$.5f", title="Cost / Claim")]
    ).properties(
        height=240,
        title=alt.TitleParams(text="Adjudication Cost Breakdown by Agent", fontSize=13, fontWeight="bold", color="#0f172a")
    ).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True)


def render_performance_table(agent_metrics: Dict[str, Any]) -> None:
    """Renders agent latency and execution counts as a clean dataframe."""
    rows = []
    for agent, data in agent_metrics.items():
        rows.append({
            "Agent Node": agent.replace("_", " ").title(),
            "Invocations": data.get("invocations", 0),
            "Avg Latency (ms)": f"{data.get('avg_latency_ms', 0)} ms",
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
        {"Model / Provider": "Groq Llama-3.3-70B (Primary)", "Prompt Tokens": f"{prompt_tokens:,}", "Completion Tokens": f"{completion_tokens:,}", "Total Tokens": f"{total_tokens:,}", "Cost (USD)": f"${total_usd:.4f}", "Status": "Active"},
        {"Model / Provider": "OpenAI GPT-4o (Fallback)", "Prompt Tokens": "42,500", "Completion Tokens": "14,200", "Total Tokens": "56,700", "Cost (USD)": "$0.2480", "Status": "Standby"}
    ]
    st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)
