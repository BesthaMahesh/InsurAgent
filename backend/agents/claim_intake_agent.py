"""
Layer 4: Agent Layer — Agent 1: Claim Intake Agent
Responsibilities:
1. Understand claim details
2. Classify claim type
3. Create structured data
4. Validate completeness & required fields
"""
from typing import Dict, Any, List
from backend.services.memory_service import MemoryService
from backend.core.logging_config import logger


class ClaimIntakeAgent:
    """
    1. Claim Intake Agent.
    Domain expert responsible for understanding unstructured claims, classifying the insurance line,
    normalizing structured data, and validating mandatory field completeness.
    """

    @staticmethod
    def process_intake(state: Dict[str, Any]) -> Dict[str, Any]:
        """Validates completeness, classifies claim type, and creates structured data."""
        claim_id = state.get("claim_id", "")
        claimant = state.get("claimant", {})
        details = state.get("claim_details", {})
        
        name = claimant.get("name", "").strip()
        policy_no = details.get("policy_number", "").strip().upper()
        raw_type = details.get("claim_type", "Health").strip()
        amount = float(details.get("amount", 0.0))
        description = details.get("description", "").strip()
        incident_date = details.get("incident_date", "")

        # 1. Understand and Classify Claim Type
        normalized_type = "Health"
        type_lower = raw_type.lower()
        if "motor" in type_lower or "car" in type_lower or "auto" in type_lower or "vehicle" in type_lower:
            normalized_type = "Motor"
        elif "travel" in type_lower or "trip" in type_lower or "flight" in type_lower:
            normalized_type = "Travel"
        elif "property" in type_lower or "home" in type_lower or "fire" in type_lower:
            normalized_type = "Property"
        else:
            normalized_type = "Health"

        # 2. Validate Completeness
        completeness_checks = {
            "has_claimant_name": bool(name),
            "has_policy_number": bool(policy_no),
            "has_valid_amount": amount > 0,
            "has_description": len(description) >= 10,
            "has_incident_date": bool(incident_date)
        }
        passed_checks = sum(1 for v in completeness_checks.values() if v)
        completeness_score = round(passed_checks / len(completeness_checks), 2)
        is_complete = completeness_score >= 0.80

        missing_fields: List[str] = [k.replace("has_", "") for k, v in completeness_checks.items() if not v]

        # 3. Create Structured Data
        normalized_details = {
            **details,
            "policy_number": policy_no,
            "claim_type": normalized_type,
            "amount": amount,
            "incident_date": incident_date,
            "description": description,
            "completeness_score": completeness_score,
            "is_complete": is_complete,
            "missing_fields": missing_fields
        }

        normalized_claimant = {
            **claimant,
            "name": name.title()
        }

        intake_data = {
            "claim_type_classification": normalized_type,
            "completeness_score": completeness_score,
            "is_complete": is_complete,
            "missing_fields": missing_fields,
            "normalized_at": "ClaimIntakeAgent"
        }

        # 4. Record to Episodic Memory
        MemoryService.record_episodic_event(
            claim_id=claim_id,
            agent="ClaimIntakeAgent",
            action=f"Classified as {normalized_type}. Completeness: {completeness_score*100:.0f}%."
        )

        logger.info(f"[ClaimIntakeAgent] Intake complete for {claim_id}: Type={normalized_type}, Score={completeness_score}")

        audit_entry = {
            "claim_id": claim_id,
            "agent": "ClaimIntakeAgent",
            "action": f"Classified claim as {normalized_type} under policy {policy_no}. Completeness Score: {completeness_score*100:.0f}%.",
            "source": "Intake Validation & Classification Engine",
            "status": "success",
            "timestamp": ""
        }

        return {
            "current_agent": "ClaimIntakeAgent",
            "claimant": normalized_claimant,
            "claim_details": normalized_details,
            "intake_data": intake_data,
            "audit_events": [audit_entry]
        }
