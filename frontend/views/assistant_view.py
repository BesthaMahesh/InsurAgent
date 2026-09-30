"""
AI Claims & Policy Assistant View for InsurAgent enterprise UI.
Directly grounded in ChromaDB policy repository, MCP Fraud bureau, and LangGraph multi-agent reasoning.
"""
import time
import textwrap
import streamlit as st
from backend.client import insuragent_client
from backend.rag.retriever import PolicyRetriever


def render_assistant_view() -> None:
    st.markdown('<div class="page-title">AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Ask questions about policies, coverage terms, exclusions, deductibles, waiting periods, and claims procedures.</div>', unsafe_allow_html=True)

    # Initialize chat history in session_state
    if "assistant_messages" not in st.session_state:
        st.session_state["assistant_messages"] = [
            {
                "role": "assistant",
                "content": "Hello! I am your InsurAgent Policy & Claims Assistant. I can help answer questions regarding coverage terms, waiting periods, deductibles, exclusion clauses, or claim adjudication files using our verified knowledge base.",
                "sources": [],
                "timestamp": "Just now"
            }
        ]

    # Quick Example Queries
    st.markdown("<div style='font-size:11.5px; font-weight:700; color:#64748b; margin-bottom:6px;'>EXAMPLE POLICY & CLAIMS QUERIES:</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    preset_q = None
    with c1:
        if st.button("✈️ Travel Shield: Covered perils & limits", use_container_width=True, key="asst_chip_1"):
            preset_q = "What are the covered perils and maximum payout limits for trip cancellation under the Travel Shield policy?"
    with c2:
        if st.button("🏥 Gold Health: Pre-existing waiting period", use_container_width=True, key="asst_chip_2"):
            preset_q = "What is the waiting period applicable to pre-existing diseases (PED) under the Gold Health Policy?"
    with c3:
        if st.button("⚠️ Explain human review for CLM-20260918-B81C", use_container_width=True, key="asst_chip_3"):
            preset_q = "Explain why claim CLM-20260918-B81C requires human review and identify all risk indicators."

    st.write("")

    # Chat Conversation History Container
    chat_container = st.container(border=True)
    with chat_container:
        for msg in st.session_state["assistant_messages"]:
            if msg["role"] == "user":
                st.markdown(textwrap.dedent(f"""
                <div class="chat-msg-user">
                    <div style="font-size:11px; color:#93c5fd; margin-bottom:4px; font-weight:700;">You</div>
                    <div>{msg['content']}</div>
                </div>
                """), unsafe_allow_html=True)
            else:
                sources_html = ""
                if msg.get("sources"):
                    sources_cards = ""
                    for s in msg["sources"]:
                        if isinstance(s, dict):
                            src_name = s.get("source_doc", "Policy Knowledge Base")
                            sec_name = s.get("section", "Coverage Schedule")
                            score = s.get("relevance_score", 0.95)
                            clause = s.get("clause_text", "")
                            sources_cards += f"""
                            <div class="source-citation-card">
                                <div style="display:flex; justify-content:space-between; margin-bottom:2px;">
                                    <b>{src_name}</b> &bull; Section: {sec_name}
                                    <span class="status-badge badge-purple" style="font-size:9.5px;">Relevance: {score}</span>
                                </div>
                                <div style="color:#475569; font-size:11px; margin-top:2px;">{clause[:160]}...</div>
                            </div>
                            """
                        else:
                            sources_cards += f'<div class="source-citation-card"><b>Source:</b> {s}</div>'

                    sources_html = f"""
                    <div style="margin-top:10px; border-top:1px solid #f1f5f9; padding-top:8px;">
                        <div style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase;">Retrieved Grounded Policy Sources (ChromaDB)</div>
                        {sources_cards}
                    </div>
                    """

                st.markdown(textwrap.dedent(f"""
                <div class="chat-msg-ai">
                    <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px;">
                        <span style="font-size:14px;">🛡️</span>
                        <span style="font-size:12px; font-weight:800; color:#0284c7;">InsurAgent Policy Assistant</span>
                        <span style="font-size:10px; color:#94a3b8; margin-left:auto;">{msg.get('timestamp', '')}</span>
                    </div>
                    <div>{msg['content']}</div>
                    {sources_html}
                </div>
                """), unsafe_allow_html=True)

    # Chat Input Box at Bottom
    with st.container():
        c_in, c_btn = st.columns([5, 1.2])
        with c_in:
            user_input = st.text_input(
                "Ask a question",
                value=preset_q if preset_q else "",
                placeholder="Ask about policy coverage, claims, exclusions, waiting periods, deductibles...",
                label_visibility="collapsed",
                key="asst_text_input_box"
            )
        with c_btn:
            ask_btn = st.button("Ask", type="primary", use_container_width=True, key="asst_send_query_btn")

    # Handle Query Submission
    if (ask_btn or preset_q) and user_input.strip():
        # Append user message
        st.session_state["assistant_messages"].append({
            "role": "user",
            "content": user_input,
            "timestamp": time.strftime("%H:%M")
        })

        progress_box = st.empty()
        with progress_box.container():
            st.markdown(textwrap.dedent("""
            <div style="background:#ffffff; border:1px solid #bfdbfe; border-radius:8px; padding:12px 16px; margin-top:8px; box-shadow:0 1px 4px rgba(2,132,199,0.06);">
                <div style="display:flex; align-items:center; gap:8px; font-weight:700; font-size:13px; color:#0369a1;">
                    <span>⏳</span> Searching policy knowledge base &amp; generating grounded response...
                </div>
            </div>
            """), unsafe_allow_html=True)

        try:
            # Query backend RAG & chat pipeline
            res = insuragent_client.post_chat(user_input)
            progress_box.empty()

            if res and not res.get("error"):
                answer = res.get("answer", "")
                
                # Fetch grounded context sources directly from ChromaDB PolicyRetriever
                try:
                    retriever = PolicyRetriever()
                    clauses = retriever.retrieve(user_input, top_k=3)
                    sources = [
                        {
                            "source_doc": c.source_doc,
                            "section": c.section,
                            "relevance_score": c.relevance_score,
                            "clause_text": c.clause_text
                        }
                        for c in clauses
                    ]
                except Exception:
                    sources = res.get("sources", [])

                st.session_state["assistant_messages"].append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "timestamp": time.strftime("%H:%M")
                })
            else:
                st.session_state["assistant_messages"].append({
                    "role": "assistant",
                    "content": "I couldn't find sufficient information in the available policy knowledge base to answer this confidently. Please review the policy document or route the question to a claims specialist.",
                    "sources": [],
                    "timestamp": time.strftime("%H:%M")
                })
        except Exception as e:
            progress_box.empty()
            st.session_state["assistant_messages"].append({
                "role": "assistant",
                "content": f"Unable to query the knowledge base at this moment: {str(e)}",
                "sources": [],
                "timestamp": time.strftime("%H:%M")
            })

        st.rerun()
