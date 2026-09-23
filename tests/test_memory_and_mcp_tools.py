import pytest
from backend.services.memory_service import MemoryService
from backend.services.governance_service import GovernanceService
from backend.mcp.client import MCPClient
from backend.mcp.tools import MCPToolRegistry
from backend.agents.supervisor_agent import SupervisorAgent
from backend.database.database import init_db


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()


def test_memory_service_episodic_and_long_term():
    # 1. Episodic Memory
    ev = MemoryService.record_episodic_event("CLM-TEST-EPI", "TestAgent", "Tested episodic recording")
    assert ev["claim_id"] == "CLM-TEST-EPI"
    
    history = MemoryService.get_episodic_history("CLM-TEST-EPI")
    assert len(history) >= 1
    assert history[0]["agent"] == "TestAgent"

    # 2. Long-term Memory
    user_mem = MemoryService.get_long_term_context("user:CUST-001")
    assert user_mem is not None
    assert user_mem["preferred_communication"] == "Email"

    # 3. Knowledge Graph
    triples = MemoryService.query_knowledge_graph("Hospital")
    assert len(triples) >= 1
    assert any("Hospital" in t["subject"] or "Hospital" in t["object"] for t in triples)


def test_all_10_mcp_tools():
    client = MCPClient()
    
    # 1. Policy Management System (API)
    r1 = client.get_policy_details("POL-HEALTH-GOLD-2026")
    assert r1["success"] is True
    assert r1["data"]["type"] == "Health"

    # 2. Claims Database (API) & GNOTHEIA
    r2 = client.get_claim_details("CLM-20260918-A12F")
    assert r2["success"] is True
    assert r2["data"]["amount"] == 125000.0

    # 3. Customer Information System
    r3 = client.get_customer_details("CUST-001")
    assert r3["success"] is True
    assert r3["data"]["name"] == "Mahesh Sharma"

    # 4. Fraud Detection Service
    r4 = client.get_risk_indicators("CLM-20260918-B81C")
    assert r4["success"] is True
    assert r4["risk_score"] > 0.50

    # 5. Enterprise Systems (ERP)
    r5 = client.query_enterprise_erp("claims_reserve")
    assert r5["success"] is True
    assert "reserve_balance_inr" in r5

    # 6. Productivity Tools (Sheets/Docs)
    r6 = client.export_claim_spreadsheet("CLM-TEST-001")
    assert r6["success"] is True
    assert "Settlement_Statement" in r6["document_name"]

    # 7. Web & External APIs (Payments & Hospital Rails)
    r7 = client.verify_hospital_and_payment_rails("Apollo Multispeciality Hospital")
    assert r7["success"] is True
    assert r7["payout_rails"]["imps_available"] is True

    # 8. File & Document Processing (Vision OCR)
    r8 = client.execute_advanced_ocr("discharge_summary.pdf", "pdf")
    assert r8["success"] is True
    assert r8["confidence"] > 0.90

    # 9. RPA Automation
    r9 = client.trigger_rpa_payout("CLM-TEST-001", 45000.0)
    assert r9["success"] is True
    assert "RPA-TASK" in r9["task_id"]

    # 10. Custom Tools (Notifications)
    r10 = client.send_notification("claimant@example.com", "Your claim is approved")
    assert r10["success"] is True
    assert r10["status"] == "Dispatched"


def test_supervisor_goal_decomposition():
    state = {
        "claim_id": "CLM-TEST-SUP",
        "claimant": {"name": "Mahesh", "customer_id": "CUST-001"},
        "claim_details": {"policy_number": "POL-HEALTH-GOLD-2026", "claim_type": "Health"},
        "query": None
    }
    plan = SupervisorAgent.plan_workflow(state)
    assert "decomposed_tasks" in plan
    assert len(plan["decomposed_tasks"]) == 7
    assert plan["current_agent"] == "SupervisorAgent"
    assert "long_term_memory" in plan


def test_governance_rbac_and_compliance():
    # RBAC checks
    assert GovernanceService.check_rbac_permission("Claimant", "submit_claim") is True
    assert GovernanceService.check_rbac_permission("Claimant", "review_hitl_queue") is False
    assert GovernanceService.check_rbac_permission("Adjuster", "review_hitl_queue") is True

    # Compliance matrix
    matrix = GovernanceService.get_regulatory_compliance_matrix()
    assert len(matrix["frameworks"]) >= 4
    assert any("IRDAI" in f["framework"] for f in matrix["frameworks"])
