from typing import List, Optional
from pydantic import BaseModel, Field


class ClaimantInfo(BaseModel):
    """Claimant contact and identity details."""
    name: str = Field(..., description="Full name of claimant", min_length=2)
    email: Optional[str] = Field(default="", description="Email address of claimant")
    phone: Optional[str] = Field(default="", description="Phone number")


class ClaimDetails(BaseModel):
    """Core parameters of an insurance claim."""
    policy_number: str = Field(..., description="Policy ID or Certificate Number", min_length=3)
    claim_type: str = Field(default="Health", description="Type of claim (Health, Motor, Travel, Property, Other)")
    amount: float = Field(..., ge=0.0, description="Claim amount claimed in INR/USD")
    incident_date: Optional[str] = Field(default="", description="Date when incident occurred (YYYY-MM-DD)")
    description: str = Field(..., description="Detailed description of the claim event", min_length=5)


class UploadedDocInfo(BaseModel):
    """Metadata of an attached supporting document."""
    filename: str
    file_type: Optional[str] = "pdf"
    content_base64: Optional[str] = None
    extracted_text: Optional[str] = None


class ClaimRequest(BaseModel):
    """API payload for submitting a new claim."""
    claim_id: Optional[str] = Field(default=None, description="Client generated or existing claim ID")
    claimant: ClaimantInfo
    claim_details: ClaimDetails
    documents: Optional[List[UploadedDocInfo]] = Field(default_factory=list)
