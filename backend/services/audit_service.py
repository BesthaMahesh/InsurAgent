import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal, AuditEventTable, init_db
from backend.models.response import AuditEventModel
from backend.core.logging_config import logger


class AuditService:
    """Service managing persistent audit trail logs."""

    @staticmethod
    def log_event(
        agent: str,
        action: str,
        claim_id: Optional[str] = None,
        source: Optional[str] = None,
        status: str = "success",
        details: Optional[str] = None,
        db: Optional[Session] = None
    ) -> AuditEventModel:
        """Persists an audit event to SQLite and logs it."""
        should_close = False
        if db is None:
            db = SessionLocal()
            should_close = True

        now_dt = datetime.datetime.now(datetime.timezone.utc)
        time_str = now_dt.strftime("%H:%M:%S")

        try:
            event_row = AuditEventTable(
                claim_id=claim_id,
                agent=agent,
                action=action,
                source=source,
                status=status,
                details=details,
                timestamp=now_dt
            )
            db.add(event_row)
            db.commit()
            db.refresh(event_row)
            
            logger.info(f"[AUDIT] [{claim_id or 'GLOBAL'}] [{agent}] {action} (Status: {status})")

            return AuditEventModel(
                claim_id=claim_id,
                agent=agent,
                action=action,
                source=source,
                status=status,
                details=details,
                timestamp=time_str
            )
        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")
            if db:
                db.rollback()
            return AuditEventModel(
                claim_id=claim_id,
                agent=agent,
                action=action,
                source=source,
                status="failed",
                details=str(e),
                timestamp=time_str
            )
        finally:
            if should_close and db:
                db.close()

    @staticmethod
    def get_events_for_claim(claim_id: str, db: Optional[Session] = None) -> List[AuditEventModel]:
        """Retrieves chronological audit events for a given claim."""
        should_close = False
        if db is None:
            db = SessionLocal()
            should_close = True

        try:
            rows = db.query(AuditEventTable).filter(AuditEventTable.claim_id == claim_id).order_by(AuditEventTable.timestamp.asc()).all()
            return [
                AuditEventModel(
                    claim_id=r.claim_id,
                    agent=r.agent,
                    action=r.action,
                    source=r.source,
                    status=r.status,
                    details=r.details,
                    timestamp=r.timestamp.strftime("%H:%M:%S") if r.timestamp else ""
                )
                for r in rows
            ]
        finally:
            if should_close and db:
                db.close()
