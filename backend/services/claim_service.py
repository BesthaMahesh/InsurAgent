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
                ClaimService.seed_default_claims(db=db)
                claim = db.query(ClaimTable).filter(ClaimTable.claim_id == claim_id).first()
                if not claim:
                    return None
            
            assessment_dict = json.loads(claim.assessment_json) if claim.assessment_json else {}
            audit_events = AuditService.get_events_for_claim(claim_id, db=db)
            doc_rows = db.query(DocumentTable).filter(DocumentTable.claim_id == claim_id).all()
            documents_list = [
                {
                    "filename": d.filename,
                    "file_type": d.file_type or d.filename.split(".")[-1],
                    "extracted_text": d.extracted_text or "",
                    "summary": d.summary or ""
                }
                for d in doc_rows
            ]

            return {
                "claim_id": claim.claim_id,
                "claimant_name": claim.claimant_name,
                "email": claim.email,
                "policy_number": claim.policy_number,
                "claim_type": claim.claim_type,
                "amount": claim.amount,
                "incident_date": claim.incident_date or (claim.created_at.strftime("%Y-%m-%d") if claim.created_at else ""),
                "description": claim.description,
                "status": claim.status,
                "recommendation": claim.recommendation,
                "confidence": claim.confidence,
                "requires_human_review": claim.requires_human_review,
                "human_review_reason": claim.human_review_reason,
                "risk_level": assessment_dict.get("risk_level", "Requires Review" if claim.requires_human_review else "Low Risk"),
                "risk_score": assessment_dict.get("risk_score", 0.68 if claim.requires_human_review else 0.12),
                "risk_indicators": assessment_dict.get("risk_indicators", []),
                "reproducibility_token": assessment_dict.get("reproducibility_token", "A7F43E2910BC"),
                "created_at": claim.created_at.isoformat() if claim.created_at else None,
                "updated_at": claim.updated_at.isoformat() if claim.updated_at else None,
                "assessment_details": assessment_dict,
                "documents": documents_list or [{"filename": f, "file_type": f.split(".")[-1]} for f in assessment_dict.get("documents", [])],
                "audit_events": [e.model_dump() for e in audit_events]
            }
        finally:
            if should_close and db:
                db.close()

    @staticmethod
    def list_recent_claims(limit: int = 20, db: Optional[Session] = None) -> List[Dict[str, Any]]:
        """Lists recent claims for dashboard display."""
        ClaimService.seed_default_claims(db=db)
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
                    "incident_date": r.incident_date or "",
                    "status": r.status,
                    "recommendation": r.recommendation,
                    "requires_human_review": r.requires_human_review,
                    "created_at": r.created_at.strftime("%Y-%m-%d") if r.created_at else ""
                }
                for r in rows
            ]
        finally:
            if should_close and db:
                db.close()

    @staticmethod
    def get_claims_by_policy_or_claimant(policy_number: str, claimant_name: str = "", exclude_claim_id: str = "", db: Optional[Session] = None) -> List[Dict[str, Any]]:
        """Retrieves previous claims for a policyholder or policy."""
        ClaimService.seed_default_claims(db=db)
        should_close = False
        if db is None:
            db = SessionLocal()
            should_close = True

        try:
            q = db.query(ClaimTable).filter(
                (ClaimTable.policy_number == policy_number) | (ClaimTable.claimant_name == claimant_name)
            )
            if exclude_claim_id:
                q = q.filter(ClaimTable.claim_id != exclude_claim_id)
            rows = q.order_by(ClaimTable.created_at.desc()).all()
            return [
                {
                    "claim_id": r.claim_id,
                    "claimant_name": r.claimant_name,
                    "policy_number": r.policy_number,
                    "claim_type": r.claim_type,
                    "amount": r.amount,
                    "incident_date": r.incident_date or "",
                    "status": r.status,
                    "recommendation": r.recommendation,
                    "requires_human_review": r.requires_human_review,
                    "created_at": r.created_at.strftime("%Y-%m-%d") if r.created_at else ""
                }
                for r in rows
            ]
        finally:
            if should_close and db:
                db.close()

    @staticmethod
    def seed_default_claims(db: Optional[Session] = None) -> None:
        """Seeds standard enterprise demonstration claims if they don't exist."""
        should_close = False
        if db is None:
            db = SessionLocal()
            should_close = True

        try:
            sample_claims = [
                {
                    "claim_id": "CLM-20260918-A12F",
                    "claimant_name": "Mahesh Sharma",
                    "email": "mahesh.sharma@example.com",
                    "policy_number": "POL-HEALTH-GOLD-2026",
                    "claim_type": "Health",
                    "amount": 125000.0,
                    "incident_date": "2026-09-10",
                    "description": "Emergency inpatient hospitalization for acute appendicitis. 3-day continuous hospital stay with laparoscopic appendectomy performed at Apollo Multispeciality Hospital.",
                    "status": "Completed",
                    "recommendation": "Recommended for Approval",
                    "confidence": 0.96,
                    "requires_human_review": False,
                    "human_review_reason": None,
                    "assessment_data": {
                        "gross_claimed": 125000.0,
                        "copay_amount": 12500.0,
                        "deductible_applied": 5000.0,
                        "non_payable_deductions": 0.0,
                        "net_payable_amount": 107500.0,
                        "recommendation": "Approved for Direct Settlement",
                        "confidence": 0.96,
                        "policy_grounding_score": 0.98,
                        "risk_level": "Low Risk",
                        "risk_score": 0.12,
                        "reproducibility_token": "A7F43E2910BC",
                        "irda_compliance": "Passed (IRDAI Health Mandate 2026)",
                        "hospital_name": "Apollo Multispeciality Hospital",
                        "documents": ["hospital_bill_apollo.pdf", "discharge_summary.pdf", "surgical_notes.pdf"]
                    }
                },
                {
                    "claim_id": "CLM-20260918-B81C",
                    "claimant_name": "Priya Patel",
                    "email": "priya.patel@example.com",
                    "policy_number": "POL-MOTOR-COMP-2026",
                    "claim_type": "Motor",
                    "amount": 82500.0,
                    "incident_date": "2026-09-15",
                    "description": "Front bumper and radiator collision damage repair estimate submitted from Apex Auto Workshop following minor road accident.",
                    "status": "Escalated",
                    "recommendation": "Requires Human Review",
                    "confidence": 0.65,
                    "requires_human_review": True,
                    "human_review_reason": "Multiple prior claims within 12 months & claim filed within 14 days of policy inception.",
                    "assessment_data": {
                        "gross_claimed": 82500.0,
                        "copay_amount": 0.0,
                        "deductible_applied": 1000.0,
                        "non_payable_deductions": 0.0,
                        "net_payable_amount": 81500.0,
                        "recommendation": "Requires Investigation",
                        "confidence": 0.65,
                        "policy_grounding_score": 0.94,
                        "risk_level": "High Risk / Requires Investigation",
                        "risk_score": 0.68,
                        "reproducibility_token": "B9C18E4420FF",
                        "irda_compliance": "Under Investigation",
                        "garage_name": "Apex Auto Workshop",
                        "risk_indicators": [
                            "Claim filed within 14 days of policy inception.",
                            "Multiple prior claims recorded across different insurers in past 12 months.",
                            "Workshop flagged for estimate discrepancies (+42% higher than standard labor rates)."
                        ],
                        "documents": ["repair_estimate_apex.pdf", "vehicle_photos.jpg", "incident_fir.pdf"]
                    }
                },
                {
                    "claim_id": "CLM-20260918-C42D",
                    "claimant_name": "Ananya Roy",
                    "email": "ananya.roy@example.com",
                    "policy_number": "POL-HEALTH-GOLD-2026",
                    "claim_type": "Health",
                    "amount": 210000.0,
                    "incident_date": "2026-09-12",
                    "description": "Elective knee arthroscopy for ligament reconstruction. High value claim requiring verification of pre-existing condition waiting period.",
                    "status": "In Review",
                    "recommendation": "Missing Document Check",
                    "confidence": 0.70,
                    "requires_human_review": True,
                    "human_review_reason": "High claimed amount (₹2.1L) and original discharge summary verification pending.",
                    "assessment_data": {
                        "gross_claimed": 210000.0,
                        "copay_amount": 21000.0,
                        "deductible_applied": 5000.0,
                        "non_payable_deductions": 0.0,
                        "net_payable_amount": 184000.0,
                        "recommendation": "Pending Discharge Summary Verification",
                        "confidence": 0.70,
                        "policy_grounding_score": 0.91,
                        "risk_level": "Medium Risk",
                        "risk_score": 0.38,
                        "reproducibility_token": "C42DE77199AA",
                        "irda_compliance": "Review in Progress",
                        "hospital_name": "Fortis Memorial Research Institute",
                        "documents": ["interim_bill.pdf", "mri_knee_report.pdf"]
                    }
                },
                {
                    "claim_id": "CLM-20260917-D73A",
                    "claimant_name": "Rahul Verma",
                    "email": "rahul.verma@example.com",
                    "policy_number": "POL-TRAVEL-SHIELD-2026",
                    "claim_type": "Travel",
                    "amount": 45000.0,
                    "incident_date": "2026-09-08",
                    "description": "International flight delay exceeding 12 hours leading to missed connecting flight and emergency hotel accommodation in Frankfurt.",
                    "status": "Completed",
                    "recommendation": "Approved for Settlement",
                    "confidence": 0.98,
                    "requires_human_review": False,
                    "human_review_reason": None,
                    "assessment_data": {
                        "gross_claimed": 45000.0,
                        "copay_amount": 0.0,
                        "deductible_applied": 0.0,
                        "non_payable_deductions": 0.0,
                        "net_payable_amount": 45000.0,
                        "recommendation": "Approved for Instant Settlement",
                        "confidence": 0.98,
                        "policy_grounding_score": 0.99,
                        "risk_level": "Low Risk",
                        "risk_score": 0.08,
                        "reproducibility_token": "D73AE89033CB",
                        "irda_compliance": "Passed",
                        "carrier_name": "Lufthansa Airlines",
                        "documents": ["boarding_pass_delay.pdf", "hotel_invoice_frankfurt.pdf"]
                    }
                }
            ]

            for s in sample_claims:
                existing = db.query(ClaimTable).filter(ClaimTable.claim_id == s["claim_id"]).first()
                if not existing:
                    claim = ClaimTable(
                        claim_id=s["claim_id"],
                        claimant_name=s["claimant_name"],
                        email=s["email"],
                        policy_number=s["policy_number"],
                        claim_type=s["claim_type"],
                        amount=s["amount"],
                        incident_date=s["incident_date"],
                        description=s["description"],
                        status=s["status"],
                        recommendation=s["recommendation"],
                        confidence=s["confidence"],
                        requires_human_review=s["requires_human_review"],
                        human_review_reason=s["human_review_reason"],
                        assessment_json=json.dumps(s["assessment_data"])
                    )
                    db.add(claim)
                    # Add document records
                    for doc_name in s["assessment_data"].get("documents", []):
                        doc_rec = DocumentTable(
                            claim_id=s["claim_id"],
                            filename=doc_name,
                            file_type=doc_name.split(".")[-1],
                            extracted_text=f"Verified supporting document {doc_name} for claim {s['claim_id']}",
                            summary=f"Automated OCR extraction verified for {doc_name}"
                        )
                        db.add(doc_rec)
            db.commit()
        except Exception as e:
            logger.warning(f"Error seeding default claims: {e}")
            if db:
                db.rollback()
        finally:
            if should_close and db:
                db.close()
