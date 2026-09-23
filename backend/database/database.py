import datetime
from sqlalchemy import create_engine, Column, String, Float, Boolean, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from backend.core.config import settings
from backend.core.logging_config import logger

def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

# SQLite connect args
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ClaimTable(Base):
    """Claim Records Table."""
    __tablename__ = "claims"

    claim_id = Column(String(64), primary_key=True, index=True)
    claimant_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    policy_number = Column(String(64), nullable=False, index=True)
    claim_type = Column(String(64), nullable=False)
    amount = Column(Float, nullable=False, default=0.0)
    incident_date = Column(String(32), nullable=True)
    description = Column(Text, nullable=False)
    status = Column(String(64), default="Intake")
    recommendation = Column(String(64), default="Pending Assessment")
    confidence = Column(Float, default=0.0)
    requires_human_review = Column(Boolean, default=False)
    human_review_reason = Column(Text, nullable=True)
    assessment_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    audit_events = relationship("AuditEventTable", back_populates="claim", cascade="all, delete-orphan")
    documents = relationship("DocumentTable", back_populates="claim", cascade="all, delete-orphan")


class AuditEventTable(Base):
    """Audit Trail Table for Enterprise Traceability & Compliance."""
    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_id = Column(String(64), ForeignKey("claims.claim_id"), nullable=True, index=True)
    agent = Column(String(64), nullable=False)
    action = Column(String(255), nullable=False)
    source = Column(String(255), nullable=True)
    status = Column(String(32), default="success")
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=utc_now)

    claim = relationship("ClaimTable", back_populates="audit_events")


class DocumentTable(Base):
    """Claim Supporting Documents."""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_id = Column(String(64), ForeignKey("claims.claim_id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(32), nullable=True)
    extracted_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    claim = relationship("ClaimTable", back_populates="documents")



def init_db():
    """Initializes the database schema."""
    logger.info("Initializing SQLite database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema initialized successfully.")


def get_db():
    """Dependency for obtaining a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
