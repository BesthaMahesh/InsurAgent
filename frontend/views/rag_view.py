"""
Knowledge Center View for InsurAgent enterprise UI.
Provides a client-facing repository of verified policy documents, coverage guidelines,
document version history tracking, and semantic knowledge search grounded in ChromaDB.
"""
import streamlit as st
import pandas as pd
from backend.rag.retriever import PolicyRetriever
from backend.client import insuragent_client
from frontend.styles import render_html


# Policy Version History Registry
POLICY_VERSION_HISTORY = {
    "Health Policy Gold Plus (POL-HEALTH-GOLD-2026)": [
        {"Version": "v3.0", "Release Date": "2026-01-01", "Status": "Active", "Changes / Revision Summary": "Updated pre-existing disease waiting period to 24 months and indexed sub-limits."},
        {"Version": "v2.0", "Release Date": "2025-01-01", "Status": "Archived", "Changes / Revision Summary": "Coverage expansion for laparoscopic appendectomy & modern treatments."},
        {"Version": "v1.0", "Release Date": "2024-01-01", "Status": "Archived", "Changes / Revision Summary": "Initial comprehensive gold health policy wording release."}
    ],
    "Motor Comprehensive Policy (POL-MOTOR-COMP-2026)": [
        {"Version": "v2.1", "Release Date": "2026-05-10", "Status": "Active", "Changes / Revision Summary": "Added zero depreciation endorsement and compulsory deductible updates."},
        {"Version": "v1.0", "Release Date": "2025-05-10", "Status": "Archived", "Changes / Revision Summary": "Standard comprehensive own-damage and third-party policy schedule."}
    ],
    "Travel Shield Policy (POL-TRAVEL-SHIELD-2026)": [
        {"Version": "v2.0", "Release Date": "2026-08-01", "Status": "Active", "Changes / Revision Summary": "Expanded trip cancellation covered perils and medical evacuation limits."},
        {"Version": "v1.0", "Release Date": "2025-08-01", "Status": "Archived", "Changes / Revision Summary": "Initial worldwide travel coverage schedule."}
    ]
}


def render_rag_view() -> None:
    """Renders the Knowledge / RAG technical developer view."""
    render_html('<div class="page-title">Knowledge / RAG</div>')
    render_html('<div class="page-subtitle">ChromaDB vector database status, dense embedding model parameters, and semantic retrieval test console.</div>')

    # ---------- Technical RAG KPIs ----------
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Vector Database", "ChromaDB v0.5.x", "Local In-Process DB")
    with c2:
        st.metric("Embedding Model", "all-MiniLM-L6-v2", "384-dimensional dense vectors")
    with c3:
        st.metric("Indexed Chunks", "41 Chunks", "500 chars / 50 overlap")
    with c4:
        st.metric("Retrieval Threshold", "Cosine Score >= 0.70", "Top-K: 4 Chunks")

    st.write("")

    # ---------- Technical RAG Architecture ----------
    with st.container(border=True):
        st.markdown("##### 🧠 RAG Architecture & Vector Space Specifications")
        render_html("""
        <div style="background:#091524; border:1px solid #1e2e42; border-radius:10px; padding:16px; margin-bottom:10px; color:#ffffff;">
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:14px; font-size:12px;">
                <div>
                    <span style="color:#94a3b8; font-size:11px; text-transform:uppercase; font-weight:700;">Vector Store Engine</span><br>
                    <b style="color:#38bdf8; font-size:13px;">ChromaDB v0.5.x</b><br>
                    <span style="color:#cbd5e1; font-size:11px;">Persistent SQLite Vector Index</span>
                </div>
                <div>
                    <span style="color:#94a3b8; font-size:11px; text-transform:uppercase; font-weight:700;">Dense Embedding Model</span><br>
                    <b style="color:#38bdf8; font-size:13px;">SentenceTransformers all-MiniLM-L6-v2</b><br>
                    <span style="color:#cbd5e1; font-size:11px;">384-dimensional normalized dense vectors</span>
                </div>
                <div>
                    <span style="color:#94a3b8; font-size:11px; text-transform:uppercase; font-weight:700;">Chunking &amp; Overlap</span><br>
                    <b style="color:#38bdf8; font-size:13px;">RecursiveCharacterTextSplitter</b><br>
                    <span style="color:#cbd5e1; font-size:11px;">Chunk Size: 500 &bull; Overlap: 50 chars</span>
                </div>
            </div>
        </div>
        """)

    st.write("")

    # ---------- Policy Library Catalog Table ----------
    with st.container(border=True):
        st.markdown("##### 📚 Indexed Document Catalog")
        
        sources_data = [
            {"Document": "Health Policy Gold Plus (POL-HEALTH-GOLD-2026)", "Category": "Health Insurance", "Version": "v3.0", "Chunks Indexed": 14, "Status": "Active", "Last Updated": "2026-09-23"},
            {"Document": "Motor Comprehensive Policy (POL-MOTOR-COMP-2026)", "Category": "Motor Insurance", "Version": "v2.1", "Chunks Indexed": 10, "Status": "Active", "Last Updated": "2026-09-23"},
            {"Document": "Travel Shield Policy (POL-TRAVEL-SHIELD-2026)", "Category": "Travel Insurance", "Version": "v2.0", "Chunks Indexed": 8, "Status": "Active", "Last Updated": "2026-09-23"},
            {"Document": "Commercial Property Policy (POL-COMM-2026)", "Category": "Property & Casualty", "Version": "v1.0", "Chunks Indexed": 4, "Status": "Active", "Last Updated": "2026-09-21"},
            {"Document": "Cyber Risk Protection Policy (POL-CYBER-2026)", "Category": "Specialty Lines", "Version": "v1.0", "Chunks Indexed": 5, "Status": "Active", "Last Updated": "2026-09-21"}
        ]
        st.dataframe(pd.DataFrame(sources_data), use_container_width=True, hide_index=True)

    st.write("")

    # ---------- Semantic Retrieval Test Console ----------
    with st.container(border=True):
        st.markdown("##### 🔬 Interactive Semantic Retrieval Test Console")
        render_html("<div style='font-size:12px; color:#64748b; margin-bottom:10px;'>Submit a test query to evaluate semantic vector retrieval, relevance scores, and LLM grounded synthesis.</div>")

        c_q, c_btn = st.columns([5, 1.2])
        with c_q:
            rag_query = st.text_input(
                "Retrieval Test Query",
                value="What is the waiting period for pre-existing diseases (PED) under the Gold Health policy?",
                placeholder="Enter query to retrieve ChromaDB vector chunks...",
                label_visibility="collapsed",
                key="dev_rag_search_input"
            )
        with c_btn:
            do_search = st.button("Search ChromaDB", type="primary", use_container_width=True, key="dev_rag_search_btn")

        if (do_search or rag_query) and rag_query.strip():
            with st.spinner("Executing ChromaDB dense vector query..."):
                retriever = PolicyRetriever()
                clauses = retriever.retrieve(rag_query, top_k=4)
                llm_res = insuragent_client.post_chat(rag_query)

            st.markdown("##### 📄 Retrieved Grounded Vector Chunks")
            if clauses:
                for idx, c in enumerate(clauses, 1):
                    clause_html = f"""
                    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px; margin-bottom:8px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <span style="font-weight:750; color:#0284c7; font-size:12.5px;">[{idx}] {c.source_doc} &bull; Section: {c.section}</span>
                            <span class="status-badge badge-purple">Cosine Relevance: {c.relevance_score:.3f}</span>
                        </div>
                        <div style="font-size:12.5px; color:#1e293b; line-height:1.5;">{c.clause_text}</div>
                    </div>
                    """
                    render_html(clause_html)
            else:
                st.info("No matching policy clauses found for this query.")

            if llm_res.get("answer"):
                st.markdown("##### 🤖 Grounded LLM Response")
                ans_text = llm_res.get('answer', '').replace("\n", "<br>")
                ans_html = f"""
                <div class="reasoning-box">
                    {ans_text}
                </div>
                """
                render_html(ans_html)

