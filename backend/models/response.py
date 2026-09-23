from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class GuardrailResult(BaseModel):
    """Result of input/output safety & compliance checks."""
    allowed: bool = True
    reasons: List[str] = Field(default_factory=list)
    pii_detected: bool = False
    prompt_injection_detected: bool = False
    sanitized_input: Optional[str] = None


class PolicyClauseEvidence(BaseModel):
    """Retrieved policy evidence snippet."""
    source_doc: str
    section: Optional[str] = None
    clause_text: str
    relevance_score: Optional[float] = None


class PolicyVerificationResult(BaseModel):
    """Verification results from RAG and policy rules."""
    policy_found: bool = True
    coverage_status: str = "Covered" # "Covered", "Excluded", "Partially Covered", "Requires Review", "Unknown"
    retrieved_clauses: List[PolicyClauseEvidence] = Field(default_factory=list)
    policy_interpretation: str = ""
    is_fabricated: bool = False


class RiskAnalysisResult(BaseModel):
    """Risk & anomaly detection output."""
    risk_level: str = "Low Risk" # "Low Risk", "Medium Risk", "High Risk", "Requires Investigation"
    risk_score: float = 0.15 # 0.0 to 1.0
    flags: List[str] = Field(default_factory=list)
    risk_summary: str = ""


class AssessmentSummary(BaseModel):
    """Final synthesis by Assessment Agent."""
    recommendation: str = "Pending Review" # "Recommended for Approval", "Recommended for Adjustment", "Requires Human Review", "Recommended for Denial"
    suggested_amount: Optional[float] = None
    confidence: float = 0.85
    reasoning: str = ""
    missing_items: List[str] = Field(default_factory=list)


class AuditEventModel(BaseModel):
    """Structured audit log entry."""
    claim_id: Optional[str] = None
    agent: str
    action: str
    source: Optional[str] = None
    status: str = "success"
    details: Optional[str] = None
    timestamp: str


class ClaimResponse(BaseModel):
    """API response after processing claim through multi-agent workflow."""
    claim_id: str
    status: str # "Completed", "Requires Human Review", "Rejected", "Processing"
    summary: str
    assessment: AssessmentSummary
    risk_analysis: RiskAnalysisResult
    policy_verification: PolicyVerificationResult
    explanation: str
    audit_events: List[AuditEventModel] = Field(default_factory=list)
    requires_human_review: bool = False
    human_review_reason: Optional[str] = None
    guardrails: Optional[GuardrailResult] = None


class ChatRequest(BaseModel):
    """User natural language query to InsurAgent."""
    query: str = Field(..., min_length=2, description="Natural language question or search query")
    claim_id: Optional[str] = None
    policy_number: Optional[str] = None


class ChatResponse(BaseModel):
    """Natural language answer produced by multi-agent reasoning."""
    answer: str
    claim_id: Optional[str] = None
    sources: List[str] = Field(default_factory=list)
    agent_actions: List[str] = Field(default_factory=list)
    confidence: float = 0.90
    requires_human_review: bool = False
    human_review_reason: Optional[str] = None
    pii_detected: bool = False
    audit_events: List[AuditEventModel] = Field(default_factory=list)
