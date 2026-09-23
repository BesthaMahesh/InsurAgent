import pytest
from backend.rag.retriever import PolicyRetriever
from backend.rag.ingest import ingest_all_documents


@pytest.fixture(scope="module", autouse=True)
def ensure_rag_ingested():
    """Ensures knowledge documents are indexed before running tests."""
    ingest_all_documents()


def test_rag_retrieval_success():
    retriever = PolicyRetriever(top_k=3)
    results = retriever.retrieve("What is the room rent and ICU limit under the Gold Health policy?")
    assert len(results) > 0
    assert any("health_policy_gold_plus.md" in r.source_doc for r in results)
    assert any("Room Rent" in r.clause_text or "ICU" in r.clause_text for r in results)


def test_rag_motor_policy_retrieval():
    retriever = PolicyRetriever(top_k=2)
    results = retriever.retrieve("depreciation on rubber, nylon, plastic parts vehicle collision")
    assert len(results) > 0
    assert any("motor_comprehensive_policy.md" in r.source_doc for r in results)


def test_rag_empty_or_gibberish_retrieval():
    retriever = PolicyRetriever(top_k=3)
    results = retriever.retrieve("xyzabc999qwerty unmatched totally unrelated token string")
    # Either returns empty or low-relevance non-fabricated
    for r in results:
        assert r.relevance_score is not None


def test_rag_context_formatting():
    retriever = PolicyRetriever()
    empty_context = retriever.format_context_for_prompt([])
    assert "NO RELEVANT POLICY EVIDENCE" in empty_context
