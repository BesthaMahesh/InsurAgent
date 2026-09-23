import pytest
from backend.agents.claim_intake_agent import ClaimIntakeAgent
from backend.agents.document_agent import DocumentAgent
from backend.agents.policy_agent import PolicyAgent
from backend.agents.risk_agent import RiskAgent
from backend.agents.assessment_agent import AssessmentAgent
from backend.agents.audit_agent import AuditAgent
from backend.database.database import init_db


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()


def test_claim_intake_agent():
    state = {
        "claim_id": "CLM-TEST-001",
        "claimant": {"name": "mahesh sharma", "email": "mahesh@test.com"},
        "claim_details": {
            "policy_number": "pol-health-gold-2026",
            "claim_type": "health insurance",
            "amount": 45000.0,
            "description": "Hospitalization for fever"
        }
    }
    res = ClaimIntakeAgent.process_intake(state)
    assert res["claimant"]["name"] == "Mahesh Sharma"
    assert res["claim_details"]["policy_number"] == "POL-HEALTH-GOLD-2026"
    assert res["claim_details"]["claim_type"] == "Health"
    assert len(res["audit_events"]) == 1


def test_document_agent_with_no_docs():
    state = {
        "claim_id": "CLM-TEST-002",
        "documents": []
    }
    res = DocumentAgent.process_documents(state)
    assert res["extracted_document_data"]["processed_count"] == 0
    assert "No supporting documents" in res["extracted_document_data"]["documents_summary"][0]


def test_policy_agent():
    agent = PolicyAgent()
    state = {
        "claim_id": "CLM-TEST-003",
        "claim_details": {
            "policy_number": "POL-HEALTH-GOLD-2026",
            "claim_type": "Health",
            "description": "Emergency hospitalization for appendicitis surgery stay 3 days."
        },
        "query": None
    }
    res = agent.verify_coverage(state)
    assert res["policy_verification"]["policy_found"] is True
    assert res["policy_verification"]["coverage_status"] in ["Covered", "Requires Review"]
    assert len(res["policy_context"]) > 0


def test_risk_agent_evaluation():
    agent = RiskAgent()
    state = {
        "claim_id": "CLM-20260918-B81C", # Mock high risk claim in MCP
        "claim_details": {"amount": 350000.0},
        "extracted_document_data": {"processed_count": 0}
    }
    res = agent.analyze_risk(state)
    assert res["risk_analysis"]["risk_level"] in ["Requires Investigation", "High Risk", "Medium Risk"]
    assert res["risk_analysis"]["risk_score"] > 0.40


def test_assessment_agent():
    state = {
        "claim_id": "CLM-TEST-004",
        "claim_details": {"claim_type": "Health", "amount": 50000.0},
        "policy_verification": {"policy_found": True, "coverage_status": "Covered"},
        "risk_analysis": {"risk_level": "Low Risk", "risk_score": 0.15},
        "extracted_document_data": {"processed_count": 1}
    }
    res = AssessmentAgent.assess_claim(state)
    assert res["assessment"]["recommendation"] == "Recommended for Approval"
    assert res["assessment"]["suggested_amount"] == 45000.0 # 50,000 - 5,000 deductible
    assert res["requires_human_review"] is False
