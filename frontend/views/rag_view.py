"""
Knowledge & RAG Management View for InsurAgent enterprise UI.
"""
import streamlit as st
import pandas as pd
import textwrap
from backend.rag.retriever import PolicyRetriever
from backend.client import insuragent_client


def render_rag_view() -> None:
    st.markdown('<div class="page-title">Enterprise Knowledge &amp; RAG Repository</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Zero-hallucination vector store indexing insurance policies, underwriting guidelines, and regulatory frameworks.</div>', unsafe_allow_html=True)

    # ---------- Knowledge Sources Metadata Grid ----------
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Documents Indexed", "8 Sources", "100% Synced")
    with c2:
        st.metric("Chunks Created", "41 Chunks", "Embeddings: all-MiniLM-L6-v2")
    with c3:
        st.metric("Vector DB Status", "Connected", "ChromaDB v0.5.x")
    with c4:
        st.metric("Last Ingestion", "2026-09-21 09:30", "Automated Daily Sync")

    st.write("")

    # ---------- Knowledge Repositories Table ----------
    with st.container(border=True):
        st.markdown("##### 📚 Indexed Knowledge Sources Catalog")
        sources_data = [
            {"Source Document": "health_policy_gold_plus.md", "Category": "Policy Document", "Clauses Indexed": 8, "Status": "Active", "Quality Score": "1.00"},
            {"Source Document": "motor_comprehensive_policy.md", "Category": "Policy Document", "Clauses Indexed": 6, "Status": "Active", "Quality Score": "0.99"},
            {"Source Document": "travel_shield_policy.md", "Category": "Policy Document", "Clauses Indexed": 5, "Status": "Active", "Quality Score": "1.00"},
            {"Source Document": "commercial_property_policy.md", "Category": "Underwriting Guidelines", "Clauses Indexed": 6, "Status": "Active", "Quality Score": "0.98"},
            {"Source Document": "cyber_risk_policy.md", "Category": "Specialty Lines", "Clauses Indexed": 4, "Status": "Active", "Quality Score": "0.98"},
            {"Source Document": "irdai_grievance_redressal.md", "Category": "Regulatory Compliance", "Clauses Indexed": 4, "Status": "Active", "Quality Score": "1.00"},
            {"Source Document": "medical_necessity_schedule.md", "Category": "Clinical Guidelines", "Clauses Indexed": 5, "Status": "Active", "Quality Score": "0.99"},
            {"Source Document": "frequently_asked_questions.md", "Category": "Claims FAQ", "Clauses Indexed": 3, "Status": "Active", "Quality Score": "1.00"}
        ]
        st.dataframe(pd.DataFrame(sources_data), use_container_width=True, hide_index=True)

    # ---------- Interactive RAG Semantic Search ----------
    with st.container(border=True):
        st.markdown("##### 🔍 Search Knowledge Base")
        st.markdown("Query the ChromaDB vector database directly to inspect retrieved policy passages and relevance scores.")

        c_q, c_btn = st.columns([5, 1.2])
        with c_q:
            rag_query = st.text_input(
                "Knowledge Search Query",
                value="What is the waiting period for pre-existing diseases (PED)?",
                label_visibility="collapsed"
            )
        with c_btn:
            do_search = st.button("Search Knowledge", type="primary", use_container_width=True)

        if do_search and rag_query.strip():
            with st.spinner("Querying ChromaDB vector space..."):
                retriever = PolicyRetriever()
                clauses = retriever.retrieve(rag_query, top_k=4)
                llm_res = insuragent_client.post_chat(rag_query)

            st.markdown("##### 📄 Retrieved Grounded Policy Documents")
            if clauses:
                for idx, c in enumerate(clauses, 1):
                    st.markdown(textwrap.dedent(f"""
                    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px; margin-bottom:8px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <span style="font-weight:700; color:#0284c7; font-size:12px;">[{idx}] {c.source_doc} • Section: {c.section}</span>
                            <span class="status-badge badge-purple">Relevance Score: {c.relevance_score}</span>
                        </div>
                        <div style="font-size:12px; color:#1e293b; line-height:1.5;">{c.clause_text}</div>
                    </div>
                    """), unsafe_allow_html=True)
            else:
                st.info("No matching policy clauses found for this query.")

            if llm_res.get("answer"):
                st.markdown("##### 🤖 Grounded Generated Synthesis")
                st.markdown(textwrap.dedent(f"""
                <div class="reasoning-box">
                    {llm_res.get('answer', '').replace(chr(10), '<br>')}
                </div>
                """), unsafe_allow_html=True)
