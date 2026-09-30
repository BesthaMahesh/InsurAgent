"""
AI Claims & Policy Assistant View for InsurAgent enterprise UI.
Features pre-RAG conversational intent handling, rapid greeting responses,
progressive retrieval loading indicators, and grounded ChromaDB policy source citations.
"""
import time
import re
import streamlit as st
from backend.client import insuragent_client
from backend.rag.retriever import PolicyRetriever
from frontend.styles import render_html


# Conversational Intent Filter
GREETING_PATTERNS = [
    r'^\s*hi\s*$', r'^\s*hello\s*$', r'^\s*hey\s*$', r'^\s*good morning\s*$',
    r'^\s*good afternoon\s*$', r'^\s*good evening\s*$', r'^\s*namaste\s*$',
    r'^\s*who are you\s*$', r'^\s*help\s*$', r'^\s*what can you do\s*$'
]

def is_greeting(query: str) -> bool:
    """Detects simple conversational greeting queries."""
    q = query.strip().lower()
    return any(re.search(pat, q) for pat in GREETING_PATTERNS)


def render_assistant_view() -> None:
    st.markdown('<div class="page-title">AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Insurance Knowledge &amp; Claims Assistant &bull; Ask questions about policies, coverage, claims, procedures, and documentation.</div>', unsafe_allow_html=True)

    # Initialize chat history in session_state
    if "assistant_messages" not in st.session_state:
        st.session_state["assistant_messages"] = [
            {
                "role": "assistant",
                "content": "Hello! I am the InsurAgent Claims & Policy Assistant. I can help you with insurance policy coverage, waiting periods, exclusions, deductibles, required claim documentation, and claim status inquiries. How can I assist you today?",
                "sources": [],
                "timestamp": "Just now"
            }
        ]

    # Quick Example Queries
    st.markdown("<div style='font-size:11.5px; font-weight:700; color:#64748b; margin-bottom:6px;'>EXAMPLE POLICY &amp; CLAIMS QUERIES:</div>", unsafe_allow_html=True)
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
                user_msg_html = f"""
                <div class="chat-msg-user">
                    <div style="font-size:11px; color:#93c5fd; margin-bottom:4px; font-weight:700;">You</div>
                    <div>{msg['content']}</div>
                </div>
                """
                render_html(user_msg_html)
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

                ai_msg_html = f"""
                <div class="chat-msg-ai">
                    <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px;">
                        <span style="font-size:14px;">🛡️</span>
                        <span style="font-size:12px; font-weight:800; color:#0284c7;">InsurAgent Policy Assistant</span>
                        <span style="font-size:10px; color:#94a3b8; margin-left:auto;">{msg.get('timestamp', '')}</span>
                    </div>
                    <div>{msg['content']}</div>
                    {sources_html}
                </div>
                """
                render_html(ai_msg_html)

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
        # Check greeting intent
        if is_greeting(user_input):
            st.session_state["assistant_messages"].append({
                "role": "user",
                "content": user_input,
                "timestamp": time.strftime("%H:%M")
            })
            st.session_state["assistant_messages"].append({
                "role": "assistant",
                "content": "Hello! I am your InsurAgent Insurance Knowledge & Claims Assistant. I can help answer questions regarding policy coverage terms, waiting periods, exclusions, deductibles, required claim documentation, and claim adjudication procedures. How can I help you today?",
                "sources": [],
                "timestamp": time.strftime("%H:%M")
            })
            st.rerun()

        # Regular Policy / Claims RAG query
        st.session_state["assistant_messages"].append({
            "role": "user",
            "content": user_input,
            "timestamp": time.strftime("%H:%M")
        })

        progress_box = st.empty()
        with progress_box.container():
            p_html = """
            <div style="background:#ffffff; border:1px solid #bfdbfe; border-radius:8px; padding:12px 16px; margin-top:8px; box-shadow:0 1px 4px rgba(2,132,199,0.06);">
                <div style="display:flex; align-items:center; gap:8px; font-weight:700; font-size:13px; color:#0369a1;">
                    <span>⏳</span> Searching policy knowledge &amp; reviewing relevant coverage information...
                </div>
            </div>
            """
            render_html(p_html)

        try:
            res = insuragent_client.post_chat(user_input)
            progress_box.empty()

            if res and not res.get("error"):
                answer = res.get("answer", "")
                
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
