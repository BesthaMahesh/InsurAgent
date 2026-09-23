import pytest
from backend.graph.workflow import process_claim_graph
from backend.database.database import init_db


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()


def test_successful_workflow_execution():
    initial_state = {
        "claim_id": "CLM-GRAPH-PASS-01",
        "claimant": {"name": "Mahesh Sharma", "email": "mahesh@test.com", "phone": "9876543210"},
        "claim_details": {
            "policy_number": "POL-HEALTH-GOLD-2026",
            "claim_type": "Health",
            "amount": 45000.0,
            "incident_date": "2026-09-10",
            "description": "Hospital stay for 3 days due to acute appendicitis surgery."
        },
        "query": None,
        "documents": [
            {
                "filename": "discharge_summary.txt",
                "extracted_text": "Discharge summary: Inpatient stay 3 days. Laparoscopic appendectomy successful."
            }
        ],
        "extracted_document_data": {},
        "policy_context": [],
        "policy_verification": {},
        "risk_analysis": {},
        "assessment": {},
        "audit_events": [],
        "messages": [],
        "current_agent": "START",
        "confidence": 0.90,
        "requires_human_review": False,
        "human_review_reason": None,
        "guardrail_result": {},
        "final_response": None,
        "errors": []
    }

    final_state = process_claim_graph(initial_state)

    assert final_state["claim_id"] == "CLM-GRAPH-PASS-01"
    assert final_state["guardrail_result"]["allowed"] is True
    assert final_state["assessment"]["recommendation"] in ["Recommended for Approval", "Recommended for Adjustment", "Requires Human Review"]
    assert len(final_state["audit_events"]) >= 4
    assert final_state["final_response"] is not None


def test_human_review_workflow_escalation():
    # Submit high-risk claim without supporting documents
    initial_state = {
        "claim_id": "CLM-20260918-B81C", # High risk claim in mock bureau
        "claimant": {"name": "Priya Patel", "email": "priya@test.com", "phone": "9811122233"},
        "claim_details": {
            "policy_number": "POL-MOTOR-COMP-2026",
            "claim_type": "Motor",
            "amount": 450000.0, # High value
            "incident_date": "2026-09-15",
            "description": "Severe front end collision on highway."
        },
        "query": None,
        "documents": [], # Missing docs
        "extracted_document_data": {},
        "policy_context": [],
        "policy_verification": {},
        "risk_analysis": {},
        "assessment": {},
        "audit_events": [],
        "messages": [],
        "current_agent": "START",
        "confidence": 0.50,
        "requires_human_review": False,
        "human_review_reason": None,
        "guardrail_result": {},
        "final_response": None,
        "errors": []
    }

    final_state = process_claim_graph(initial_state)

    assert final_state["requires_human_review"] is True
    assert final_state["human_review_reason"] is not None
    assert any(e["agent"] == "HumanReviewCheck" or "Human Review" in e["action"] for e in final_state["audit_events"])
