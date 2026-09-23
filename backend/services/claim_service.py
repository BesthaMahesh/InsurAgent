import json
import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal, ClaimTable, DocumentTable
from backend.models.claim import ClaimRequest
from backend.models.response import ClaimResponse, AssessmentSummary, RiskAnalysisResult, PolicyVerificationResult
from backend.services.audit_service import AuditService
from backend.core.logging_config import logger


class ClaimService:
    """Service to create, update, and search claims in SQLite."""

    @staticmethod
    def save_or_update_claim(
        claim_id: str,
        claimant_name: str,
        policy_number: str,
        claim_type: str,
        amount: float,
        description: str,
        email: str = "",
        incident_date: str = "",
        status: str = "Completed",
        recommendation: str = "Pending Review",
        confidence: float = 0.85,
        requires_human_review: bool = False,
        human_review_reason: Optional[str] = None,
        assessment_data: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None
    ) -> ClaimTable:
        """Saves or updates a claim record in SQLite."""
        should_close = False
        if db is None:
            db = SessionLocal()
            should_close = True

        try:
            claim = db.query(ClaimTable).filter(ClaimTable.claim_id == claim_id).first()
            if not claim:
                claim = ClaimTable(
                    claim_id=claim_id,
                    claimant_name=claimant_name,
                    email=email,
                    policy_number=policy_number,
                    claim_type=claim_type,
                    amount=amount,
                    incident_date=incident_date,
                    description=description,
                    status=status,
                    recommendation=recommendation,
                    confidence=confidence,
                    requires_human_review=requires_human_review,
                    human_review_reason=human_review_reason,
                    assessment_json=json.dumps(assessment_data or {})
                )
                db.add(claim)
            else:
                claim.claimant_name = claimant_name
                claim.email = email
                claim.policy_number = policy_number
                claim.claim_type = claim_type
                claim.amount = amount
                claim.incident_date = incident_date
                claim.description = description
                claim.status = status
                claim.recommendation = recommendation
                claim.confidence = confidence
                claim.requires_human_review = requires_human_review
                claim.human_review_reason = human_review_reason
                claim.assessment_json = json.dumps(assessment_data or {})
                claim.updated_at = datetime.datetime.now(datetime.timezone.utc)

            db.commit()
            db.refresh(claim)
            return claim
        except Exception as e:
            logger.error(f"Error saving claim {claim_id}: {e}")
            if db:
                db.rollback()
            raise
        finally:
            if should_close and db:
                db.close()

    @staticmethod
    def get_claim(claim_id: str, db: Optional[Session] = None) -> Optional[Dict[str, Any]]:
        """Retrieves a claim and its parsed assessment details."""
        should_close = False
        if db is None:
            db = SessionLocal()
            should_close = True

        try:
            claim = db.query(ClaimTable).filter(ClaimTable.claim_id == claim_id).first()
            if not claim:
                return None
            
            assessment_dict = json.loads(claim.assessment_json) if claim.assessment_json else {}
            audit_events = AuditService.get_events_for_claim(claim_id, db=db)

            return {
                "claim_id": claim.claim_id,
                "claimant_name": claim.claimant_name,
                "email": claim.email,
                "policy_number": claim.policy_number,
                "claim_type": claim.claim_type,
                "amount": claim.amount,
                "incident_date": claim.incident_date,
                "description": claim.description,
                "status": claim.status,
                "recommendation": claim.recommendation,
                "confidence": claim.confidence,
                "requires_human_review": claim.requires_human_review,
                "human_review_reason": claim.human_review_reason,
                "created_at": claim.created_at.isoformat() if claim.created_at else None,
                "updated_at": claim.updated_at.isoformat() if claim.updated_at else None,
                "assessment_details": assessment_dict,
                "audit_events": [e.model_dump() for e in audit_events]
            }
        finally:
            if should_close and db:
                db.close()

    @staticmethod
    def list_recent_claims(limit: int = 10, db: Optional[Session] = None) -> List[Dict[str, Any]]:
        """Lists recent claims for dashboard display."""
        should_close = False
        if db is None:
            db = SessionLocal()
            should_close = True

        try:
            rows = db.query(ClaimTable).order_by(ClaimTable.created_at.desc()).limit(limit).all()
            return [
                {
                    "claim_id": r.claim_id,
                    "claimant_name": r.claimant_name,
                    "policy_number": r.policy_number,
                    "claim_type": r.claim_type,
                    "amount": r.amount,
                    "status": r.status,
                    "recommendation": r.recommendation,
                    "requires_human_review": r.requires_human_review,
                    "created_at": r.created_at.isoformat() if r.created_at else ""
                }
                for r in rows
            ]
        finally:
            if should_close and db:
                db.close()
