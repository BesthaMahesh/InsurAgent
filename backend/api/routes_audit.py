from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.response import AuditEventModel
from backend.services.audit_service import AuditService
from backend.database.database import get_db

router = APIRouter(prefix="/api/audit", tags=["Audit Trail"])


@router.get("/{claim_id}", response_model=List[AuditEventModel])
def get_audit_trail(claim_id: str, db: Session = Depends(get_db)):
    """
    Returns complete chronological audit log entries for a given claim.
    """
    events = AuditService.get_events_for_claim(claim_id, db=db)
    if not events:
        # Check if generic events or empty
        return []
    return events
