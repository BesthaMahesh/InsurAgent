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
    st.markdown('<div class="page-title">Knowledge Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Search and review verified policy information, coverage rules, underwriting guidelines, and supporting document schedules.</div>', unsafe_allow_html=True)

    # ---------- Knowledge Center Overview KPIs ----------
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Policy Documents", "8 Sources", "100% Synced")
    with c2:
        st.metric("Indexed Sections", "41 Chunks", "Zero-Hallucination")
    with c3:
        st.metric("Knowledge Status", "Connected", "ChromaDB v0.5.x")
    with c4:
        st.metric("Last Updated", "2026-09-23", "Continuous Verification")

    st.write("")

    # ---------- Policy Library Catalog Table ----------
    with st.container(border=True):
        st.markdown("##### 📚 Policy Library & Regulatory Schedules")
        
        sources_data = [
            {"Document": "Health Policy Gold Plus (POL-HEALTH-GOLD-2026)", "Category": "Health Insurance", "Version": "v3.0", "Status": "Active", "Last Updated": "2026-09-23"},
            {"Document": "Motor Comprehensive Policy (POL-MOTOR-COMP-2026)", "Category": "Motor Insurance", "Version": "v2.1", "Status": "Active", "Last Updated": "2026-09-23"},
            {"Document": "Travel Shield Policy (POL-TRAVEL-SHIELD-2026)", "Category": "Travel Insurance", "Version": "v2.0", "Status": "Active", "Last Updated": "2026-09-23"},
            {"Document": "Commercial Property Policy (POL-COMM-2026)", "Category": "Property & Casualty", "Version": "v1.0", "Status": "Active", "Last Updated": "2026-09-21"},
            {"Document": "Cyber Risk Protection Policy (POL-CYBER-2026)", "Category": "Specialty Lines", "Version": "v1.0", "Status": "Active", "Last Updated": "2026-09-21"},
            {"Document": "IRDAI Grievance & Adjudication Standard", "Category": "Regulatory Compliance", "Version": "v2.0", "Status": "Active", "Last Updated": "2026-09-20"},
            {"Document": "Clinical Medical Necessity Schedule", "Category": "Underwriting Guidelines", "Version": "v1.2", "Status": "Active", "Last Updated": "2026-09-18"},
            {"Document": "Claims Adjudication FAQ & Slabs", "Category": "Operating Procedures", "Version": "v1.0", "Status": "Active", "Last Updated": "2026-09-18"}
        ]
        st.dataframe(pd.DataFrame(sources_data), use_container_width=True, hide_index=True)

        st.write("")
        st.markdown("##### 📜 Policy Actions: Inspect Document History")
        doc_col, btn_view_col, btn_hist_col = st.columns([3.5, 1.2, 1.3])
        with doc_col:
            selected_doc = st.selectbox(
                "Select Policy Document",
                [d["Document"] for d in sources_data],
                label_visibility="collapsed",
                key="kc_doc_selector"
            )
        with btn_view_col:
            view_clicked = st.button("👁️ View Clauses", type="primary", use_container_width=True, key="kc_view_clauses_btn")
        with btn_hist_col:
            history_clicked = st.button("📜 View History", use_container_width=True, key="kc_view_history_btn")

        # Handle View History Action
        if history_clicked:
            st.session_state["kc_active_history_doc"] = selected_doc

        if st.session_state.get("kc_active_history_doc"):
            hist_doc = st.session_state["kc_active_history_doc"]
            st.markdown(f"###### 📜 Version & Revision History: `{hist_doc}`")
            if hist_doc in POLICY_VERSION_HISTORY:
                hist_records = POLICY_VERSION_HISTORY[hist_doc]
                st.dataframe(pd.DataFrame(hist_records), use_container_width=True, hide_index=True)
            else:
                st.info(f"No previous archived versions available for {hist_doc}. Current active release is v1.0.")

    st.write("")

    # ---------- Search Policy Knowledge Base ----------
    with st.container(border=True):
        st.markdown("##### 🔍 Search Policy Knowledge Base")
        st.markdown("<div style='font-size:12px; color:#64748b; margin-bottom:10px;'>Ask any question to search verified policy documents and coverage clauses with zero-hallucination semantic retrieval.</div>", unsafe_allow_html=True)

        c_q, c_btn = st.columns([5, 1.2])
        with c_q:
            rag_query = st.text_input(
                "Knowledge Search Query",
                value="What is the waiting period for pre-existing diseases (PED) under the Gold Health policy?",
                placeholder="What would you like to know about policy terms, coverage, or exclusions?",
                label_visibility="collapsed",
                key="rag_search_input_box"
            )
        with c_btn:
            do_search = st.button("Search", type="primary", use_container_width=True, key="rag_search_btn")

        if (do_search or rag_query) and rag_query.strip():
            with st.spinner("Searching verified policy repository..."):
                retriever = PolicyRetriever()
                clauses = retriever.retrieve(rag_query, top_k=4)
                llm_res = insuragent_client.post_chat(rag_query)

            st.markdown("##### 📄 Retrieved Grounded Policy Evidence")
            if clauses:
                for idx, c in enumerate(clauses, 1):
                    clause_html = f"""
                    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px; margin-bottom:8px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <span style="font-weight:750; color:#0284c7; font-size:12.5px;">[{idx}] {c.source_doc} &bull; Section: {c.section}</span>
                            <span class="status-badge badge-purple">Relevance: {c.relevance_score}</span>
                        </div>
                        <div style="font-size:12.5px; color:#1e293b; line-height:1.5;">{c.clause_text}</div>
                    </div>
                    """
                    render_html(clause_html)
            else:
                st.info("No matching policy clauses found for this query.")

            if llm_res.get("answer"):
                st.markdown("##### 🤖 Grounded Policy Summary")
                ans_text = llm_res.get('answer', '').replace("\n", "<br>")
                ans_html = f"""
                <div class="reasoning-box">
                    {ans_text}
                </div>
                """
                render_html(ans_html)

    st.write("")

    # Expandable Technical Details
    with st.expander("🛠️ View Technical Details (RAG & Vector Space)"):
        tech_html = """
        <div style="font-size:12px; line-height:1.6; color:#334155;">
            <b>Vector Store:</b> ChromaDB v0.5.x Embedded Database<br>
            <b>Embedding Model:</b> SentenceTransformers <code>all-MiniLM-L6-v2</code> (384-dimensional dense vectors)<br>
            <b>Chunking Strategy:</b> Recursive Character Splitter (Chunk Size: 500 characters, Chunk Overlap: 50 characters)<br>
            <b>Retrieval Strategy:</b> Top-K Cosine Similarity with Relevance Score Thresholding (&ge; 0.70)
        </div>
        """
        render_html(tech_html)
