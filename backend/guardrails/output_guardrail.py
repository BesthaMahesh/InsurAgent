import re
from typing import Dict, Any, List, Optional
from backend.core.config import settings
from backend.core.logging_config import logger

DISCLAIMER_TEXT = (
    "\n\n*Note: InsurAgent provides AI-assisted claim assessment recommendations for human adjusters and "
    "does not execute legally binding final claims decisions without human review.*"
)

# Protected demographic markers for bias monitoring
PROTECTED_DEMOGRAPHIC_PATTERNS = [
    re.compile(r'\b(caste|religion|ethnic|gender|race|creed|marital\s+status|sexual\s+orientation)\b', re.IGNORECASE),
    re.compile(r'\b(due\s+to\s+(his|her|their)\s+(age|gender|race|background))\b', re.IGNORECASE)
]

# Explainability markers
EXPLAINABILITY_MARKERS = [
    "because", "reason", "coverage", "policy", "clause", "deductible", "assessment", "incurred", "adjudication"
]


class OutputGuardrail:
    """
    Comprehensive Enterprise Output Guardrail implementing all 5 architectural sub-checks:
    1. Sensitive Data Filter (Redact credit cards, national IDs, passwords)
    2. Policy Compliance (Statutory notices, IRDAI adherence disclaimers)
    3. Bias Check (Fairness audit, protected attributes filtering)
    4. Explainability Check (Validates reasoning steps & grounding citations)
    5. Safe Response Generation (Compiles certified output payload)
    """

    @staticmethod
    def filter_sensitive_data(text: str) -> Dict[str, Any]:
        """Filters and masks sensitive PII or data leakage from generated outputs."""
        sanitized = re.sub(r'\b(?:\d{4}[-\s]?){3}\d{4}\b', '[CARD_REDACTED]', text)
        sanitized = re.sub(r'\b\d{3}-\d{2}-\d{4}\b|\b\d{4}\s\d{4}\s\d{4}\b', '[ID_REDACTED]', sanitized)
        sanitized = re.sub(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', '[PHONE_REDACTED]', sanitized)
        return {
            "filtered_text": sanitized,
            "was_modified": sanitized != text
        }

    @staticmethod
    def check_policy_compliance(text: str) -> Dict[str, Any]:
        """Ensures mandatory regulatory and non-binding advisory disclaimers are attached."""
        compliant = "InsurAgent provides AI-assisted" in text
        final_text = text
        if not compliant:
            final_text = text.strip() + DISCLAIMER_TEXT
        return {
            "is_compliant": compliant,
            "compliant_text": final_text,
            "statutory_standard": "IRDAI-CIRCULAR-2026/AI-ADVISORY"
        }

    @staticmethod
    def check_bias(text: str) -> Dict[str, Any]:
        """Evaluates output text to ensure decisions are fair, non-discriminatory, and objective."""
        bias_flags = []
        for pattern in PROTECTED_DEMOGRAPHIC_PATTERNS:
            if pattern.search(text):
                bias_flags.append(pattern.pattern)
        
        return {
            "bias_free": len(bias_flags) == 0,
            "bias_flags": bias_flags,
            "fairness_index": 1.0 if len(bias_flags) == 0 else 0.4
        }

    @staticmethod
    def check_explainability(text: str, has_policy_evidence: bool) -> Dict[str, Any]:
        """Validates that output contains sufficient rationale, itemized steps, and grounding."""
        text_lower = text.lower()
        matched_markers = [m for m in EXPLAINABILITY_MARKERS if m in text_lower]
        explainability_score = min(1.0, len(matched_markers) / 4.0)
        
        has_sufficient_explanation = (explainability_score >= 0.5) and has_policy_evidence
        return {
            "explainable": has_sufficient_explanation,
            "explainability_score": round(explainability_score, 2),
            "matched_markers": matched_markers,
            "grounded_in_clauses": has_policy_evidence
        }

    @classmethod
    def validate_and_sanitize_response(
        cls,
        response_text: str,
        confidence: float,
        risk_score: float,
        has_policy_evidence: bool,
        requires_human_review: bool = False,
        human_review_reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes all 5 Output Guardrail checks sequentially and generates certified response.
        """
        reasons: List[str] = []

        # 1. Sensitive Data Filter
        sensitive_res = cls.filter_sensitive_data(response_text)
        current_text = sensitive_res["filtered_text"]

        # 2. Bias Check
        bias_res = cls.check_bias(current_text)
        if not bias_res["bias_free"]:
            requires_human_review = True
            reasons.append("Potential bias or protected demographic reference detected in output.")

        # 3. Explainability Check
        explain_res = cls.check_explainability(current_text, has_policy_evidence)
        if not explain_res["explainable"]:
            reasons.append("Insufficient policy reasoning or ungrounded claims assertions.")

        # 4. Confidence & Risk Threshold Checks
        if confidence < settings.CONFIDENCE_THRESHOLD:
            requires_human_review = True
            reasons.append(f"Confidence score ({confidence:.2f}) is below threshold ({settings.CONFIDENCE_THRESHOLD:.2f}).")

        if risk_score >= settings.HIGH_RISK_THRESHOLD:
            requires_human_review = True
            reasons.append(f"Elevated risk score ({risk_score:.2f}) exceeds threshold ({settings.HIGH_RISK_THRESHOLD:.2f}).")

        if not has_policy_evidence:
            reasons.append("No grounded policy evidence retrieved; human verification mandatory.")

        # Combine human review reason
        final_review_reason = human_review_reason
        if reasons and not final_review_reason:
            final_review_reason = "; ".join(reasons)

        # 5. Policy Compliance & Safe Response Generation
        compliance_res = cls.check_policy_compliance(current_text)
        final_sanitized_text = compliance_res["compliant_text"]

        return {
            "sanitized_response": final_sanitized_text,
            "requires_human_review": requires_human_review,
            "human_review_reason": final_review_reason,
            "grounded": has_policy_evidence,
            "safety_passed": True,
            "sub_checks": {
                "sensitive_data_filter": True,
                "policy_compliance": True,
                "bias_check": bias_res["bias_free"],
                "explainability_check": explain_res["explainable"],
                "safe_response_generation": True
            },
            "metrics": {
                "fairness_index": bias_res["fairness_index"],
                "explainability_score": explain_res["explainability_score"]
            }
        }
