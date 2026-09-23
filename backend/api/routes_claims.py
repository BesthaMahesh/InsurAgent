import uuid
import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models.claim import ClaimRequest
from backend.models.response import ClaimResponse, AssessmentSummary, RiskAnalysisResult, PolicyVerificationResult, AuditEventModel, GuardrailResult
from backend.services.claim_service import ClaimService
from backend.services.audit_service import AuditService
from backend.graph.workflow import process_claim_graph
from backend.database.database import get_db
from backend.core.logging_config import logger

router = APIRouter(prefix="/api/claims", tags=["Claims"])


@router.post("/process", response_model=ClaimResponse)
def process_claim(request: ClaimRequest, db: Session = Depends(get_db)):
    """
    Submits a claim for complete multi-agent LangGraph workflow processing.
    """
    claim_id = request.claim_id or f"CLM-{datetime.datetime.now():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}"
    
    logger.info(f"Received claim process request for {claim_id}")

    initial_state = {
        "claim_id": claim_id,
        "claimant": request.claimant.model_dump(),
        "claim_details": request.claim_details.model_dump(),
        "query": None,
        "documents": [d.model_dump() for d in (request.documents or [])],
        "extracted_document_data": {},
        "policy_context": [],
        "policy_verification": {},
        "risk_analysis": {},
        "assessment": {},
        "audit_events": [],
        "messages": [],
        "current_agent": "START",
        "confidence": 0.85,
        "requires_human_review": False,
        "human_review_reason": None,
        "guardrail_result": {},
        "final_response": None,
        "errors": []
    }

    # Execute LangGraph workflow
    try:
        final_state = process_claim_graph(initial_state)
    except Exception as e:
        logger.error(f"Error executing claim graph: {e}")
        raise HTTPException(status_code=500, detail=f"Graph execution failed: {str(e)}")

    assessment_data = final_state.get("assessment", {})
    risk_data = final_state.get("risk_analysis", {})
    policy_data = final_state.get("policy_verification", {})
    guardrail_data = final_state.get("guardrail_result", {})
    requires_review = final_state.get("requires_human_review", False)
    review_reason = final_state.get("human_review_reason")

    status_str = "Requires Human Review" if requires_review else "Completed"
    recommendation_str = assessment_data.get("recommendation", "Pending Review")

    # Persist claim in database
    ClaimService.save_or_update_claim(
        claim_id=claim_id,
        claimant_name=request.claimant.name,
        email=request.claimant.email or "",
        policy_number=request.claim_details.policy_number,
        claim_type=request.claim_details.claim_type,
        amount=request.claim_details.amount,
        incident_date=request.claim_details.incident_date or "",
        description=request.claim_details.description,
        status=status_str,
        recommendation=recommendation_str,
        confidence=float(final_state.get("confidence", 0.85)),
        requires_human_review=requires_review,
        human_review_reason=review_reason,
        assessment_data={
            "assessment": assessment_data,
            "risk": risk_data,
            "policy": policy_data
        },
        db=db
    )

    # Fetch stored audit events
    audit_models = AuditService.get_events_for_claim(claim_id, db=db)

    return ClaimResponse(
        claim_id=claim_id,
        status=status_str,
        summary=f"Claim for {request.claimant.name} ({request.claim_details.claim_type} - INR {request.claim_details.amount:,.2f}) assessed with status: {status_str}.",
        assessment=AssessmentSummary(**assessment_data) if assessment_data else AssessmentSummary(recommendation=recommendation_str),
        risk_analysis=RiskAnalysisResult(**risk_data) if risk_data else RiskAnalysisResult(),
        policy_verification=PolicyVerificationResult(**policy_data) if policy_data else PolicyVerificationResult(policy_found=False),
        explanation=final_state.get("final_response", ""),
        audit_events=audit_models,
        requires_human_review=requires_review,
        human_review_reason=review_reason,
        guardrails=GuardrailResult(**guardrail_data) if guardrail_data else GuardrailResult()
    )


@router.get("/recent")
def list_claims(limit: int = 10, db: Session = Depends(get_db)):
    """Lists recent claims for dashboard display."""
    return ClaimService.list_recent_claims(limit=limit, db=db)


@router.get("/{claim_id}")
def get_claim(claim_id: str, db: Session = Depends(get_db)):
    """Retrieves full claim details, risk analysis, and audit events."""
    claim = ClaimService.get_claim(claim_id, db=db)
    if not claim:
        raise HTTPException(status_code=404, detail=f"Claim {claim_id} not found.")
    return claim
