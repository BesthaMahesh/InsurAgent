from fastapi import APIRouter
from typing import Dict, Any
from backend.services.governance_service import GovernanceService
from backend.services.evaluation_service import EvaluationService
from backend.services.cost_service import CostService
from backend.services.observability_service import ObservabilityService

router = APIRouter(prefix="/api/governance", tags=["Responsible AI & Governance"])


@router.get("/overview")
def get_governance_overview() -> Dict[str, Any]:
    """Returns Responsible AI governance metrics, data catalog, and model status."""
    return {
        "data_governance": GovernanceService.get_data_governance_report(),
        "bias_fairness": GovernanceService.evaluate_fairness(),
        "model_governance": GovernanceService.get_model_governance_report()
    }


@router.post("/adversarial-test")
def run_adversarial_testing() -> Dict[str, Any]:
    """Runs automated adversarial attack simulations and returns robustness score."""
    return GovernanceService.run_adversarial_test_suite()


@router.get("/cost-analysis")
def get_cost_analysis() -> Dict[str, Any]:
    """Returns token usage telemetry, cost per claim, and budget metrics."""
    return CostService.get_aggregate_cost_metrics()


@router.get("/observability")
def get_observability_metrics() -> Dict[str, Any]:
    """Returns live telemetry on agent latencies, tool calls, and anomaly alerts."""
    return ObservabilityService.get_dashboard_telemetry()


@router.get("/compliance-report")
def get_compliance_report() -> Dict[str, Any]:
    """Generates automated regulatory compliance report for IRDAI auditors."""
    return ObservabilityService.generate_automated_compliance_report()
