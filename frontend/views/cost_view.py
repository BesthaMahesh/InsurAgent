"""
Cost & Token Usage View for InsurAgent enterprise UI.
"""
import streamlit as st
import pandas as pd
from backend.client import insuragent_client
from frontend.components.cards import render_kpi_card
from frontend.components.charts import render_cost_breakdown_table


def render_cost_view() -> None:
    st.markdown('<div class="page-title">Cost &amp; Token Usage Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Granular token consumption tracking, prompt caching efficiencies, and estimated LLM API expenditure.</div>', unsafe_allow_html=True)

    cost_data = insuragent_client.get_cost_analysis()
    total_tokens = cost_data.get("total_tokens_consumed", 1420800)
    prompt_tokens = int(total_tokens * 0.68)
    completion_tokens = total_tokens - prompt_tokens
    total_usd = cost_data.get("total_cost_usd", 1.04)
    avg_per_claim = cost_data.get("average_cost_per_claim_usd", 0.00162)

    # ---------- Top Cost KPIs ----------
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Total Tokens", f"{total_tokens:,}", f"Input: {prompt_tokens:,} | Output: {completion_tokens:,}", "Estimated", "blue", is_demo=True)
    with c2:
        render_kpi_card("Total LLM Cost", f"${total_usd:.4f}", f"₹{total_usd*86.5:.2f} INR", "Budget 99.8% Left", "green", is_demo=True)
    with c3:
        render_kpi_card("Avg Cost / Claim", f"${avg_per_claim:.5f}", f"₹{avg_per_claim*86.5:.3f} INR", "Optimized", "purple", is_demo=True)
    with c4:
        render_kpi_card("Avg Cost / Workflow", f"${avg_per_claim*1.1:.5f}", "Full 6-agent DAG invocation", "Target Met", "navy", is_demo=True)

    st.write("")

    # ---------- Cost Breakdown by Agent Table ----------
    with st.container(border=True):
        st.markdown("##### 💰 Estimated Cost Breakdown by Agent Node")
        agent_costs = [
            {"Agent Node": "Claim Intake Agent", "Avg Tokens / Run": 380, "Cost / Run (USD)": "$0.00022", "Optimization": "Structured Pydantic Extraction"},
            {"Agent Node": "Document Analysis Agent", "Avg Tokens / Run": 650, "Cost / Run (USD)": "$0.00038", "Optimization": "Local Vision OCR Pre-filtering"},
            {"Agent Node": "Policy Verification Agent", "Avg Tokens / Run": 820, "Cost / Run (USD)": "$0.00048", "Optimization": "ChromaDB Top-3 Chunk Truncation"},
            {"Agent Node": "Fraud / Risk Agent", "Avg Tokens / Run": 240, "Cost / Run (USD)": "$0.00014", "Optimization": "Deterministic Rules & MCP API"},
            {"Agent Node": "Claim Assessment Agent", "Avg Tokens / Run": 710, "Cost / Run (USD)": "$0.00042", "Optimization": "Concise CoT Prompt Template"},
            {"Agent Node": "Audit & Compliance Agent", "Avg Tokens / Run": 120, "Cost / Run (USD)": "$0.00007", "Optimization": "Local Python SHA-256 Hashing"}
        ]
        st.dataframe(pd.DataFrame(agent_costs), use_container_width=True, hide_index=True)

    # Active Provider Catalog
    with st.container(border=True):
        st.markdown("##### 🔌 Active Model & Pricing Catalog")
        render_cost_breakdown_table(cost_data)
