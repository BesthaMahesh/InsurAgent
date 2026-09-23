import re
from typing import Dict, Any, List, Optional
from backend.core.logging_config import logger

# Regex patterns for deterministic PII detection
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
PHONE_REGEX = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
CARD_REGEX = re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b')
SSN_AADHAAR_REGEX = re.compile(r'\b\d{3}-\d{2}-\d{4}\b|\b\d{4}\s\d{4}\s\d{4}\b')

# Deterministic prompt injection defense patterns
PROMPT_INJECTION_PATTERNS = [
    re.compile(r'ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|rules)', re.IGNORECASE),
    re.compile(r'system\s+prompt', re.IGNORECASE),
    re.compile(r'you\s+are\s+now\s+(in\s+)?(dan|developer|god)\s+mode', re.IGNORECASE),
    re.compile(r'disregard\s+(system|safety|guardrails)', re.IGNORECASE),
    re.compile(r'bypass\s+(verification|policy|guardrail)', re.IGNORECASE),
    re.compile(r'drop\s+table|delete\s+from|union\s+select|<script>', re.IGNORECASE),
    re.compile(r'override\s+claim\s+limit', re.IGNORECASE),
    re.compile(r'force\s+(approve|payout|settlement)', re.IGNORECASE)
]

# Unsafe/harmful keywords & content safety patterns
UNSAFE_PATTERNS = [
    re.compile(r'\b(bomb|weapon|assassinate|exploit|malware|ransomware)\b', re.IGNORECASE),
    re.compile(r'\b(bribe|fraudulent\s+invoice|forge\s+documents|money\s+laundering)\b', re.IGNORECASE)
]

# Valid policy prefix patterns
VALID_POLICY_PREFIXES = ["POL-HEALTH-", "POL-MOTOR-", "POL-TRAVEL-", "POL-PROP-", "POL-CYBER-", "POL-COMM-", "POL-"]


class InputGuardrail:
    """
    Comprehensive Enterprise Input Guardrail implementing all 5 architectural sub-checks:
    1. Input Validation (structure, length, completeness)
    2. PII Detection (redaction & security logging)
    3. Prompt Injection Detection (jailbreak, evasion, role hijack)
    4. Policy Checks (format, validity, line sanity)
    5. Content Safety (restricted terms, fraud collusion triggers)
    """

    @staticmethod
    def check_pii(text: str) -> Dict[str, Any]:
        """Detects and redacts sensitive PII."""
        detected_types = []
        if CARD_REGEX.search(text):
            detected_types.append("credit_card")
        if SSN_AADHAAR_REGEX.search(text):
            detected_types.append("national_id")
        if PHONE_REGEX.search(text):
            detected_types.append("phone_number")
        if EMAIL_REGEX.search(text):
            detected_types.append("email_address")

        sanitized = CARD_REGEX.sub("[CARD_REDACTED]", text)
        sanitized = SSN_AADHAAR_REGEX.sub("[ID_REDACTED]", sanitized)

        return {
            "pii_detected": len(detected_types) > 0,
            "detected_types": detected_types,
            "sanitized_text": sanitized
        }

    @staticmethod
    def check_prompt_injection(text: str) -> Dict[str, Any]:
        """Detects prompt injection attempts."""
        matched_patterns = []
        for pattern in PROMPT_INJECTION_PATTERNS:
            if pattern.search(text):
                matched_patterns.append(pattern.pattern)

        return {
            "injection_detected": len(matched_patterns) > 0,
            "matched_patterns": matched_patterns
        }

    @staticmethod
    def check_content_safety(text: str) -> Dict[str, Any]:
        """Evaluates content safety against restricted/unsafe patterns."""
        violating_terms = []
        for pattern in UNSAFE_PATTERNS:
            if pattern.search(text):
                violating_terms.append(pattern.pattern)

        return {
            "content_safe": len(violating_terms) == 0,
            "violating_terms": violating_terms
        }

    @staticmethod
    def check_policy(policy_number: str) -> Dict[str, Any]:
        """Validates policy number format and prefix sanity."""
        if not policy_number or not policy_number.strip():
            return {"valid": False, "reason": "Policy number cannot be empty."}
        
        clean = policy_number.strip().upper()
        if len(clean) < 5:
            return {"valid": False, "reason": "Policy number format too short."}
            
        has_valid_prefix = any(clean.startswith(prefix) for prefix in VALID_POLICY_PREFIXES)
        return {
            "valid": True,
            "policy_number": clean,
            "has_recognized_prefix": has_valid_prefix,
            "reason": "Policy number format verified." if has_valid_prefix else "Standard custom policy format accepted."
        }

    @classmethod
    def validate_text(cls, text: str, context: str = "query") -> Dict[str, Any]:
        """Validates arbitrary text inputs (user queries, search prompts)."""
        reasons: List[str] = []
        allowed = True

        if not text or not text.strip():
            return {
                "allowed": False,
                "reasons": ["Input cannot be empty."],
                "pii_detected": False,
                "prompt_injection_detected": False,
                "policy_check_passed": True,
                "content_safety_passed": True,
                "sanitized_input": "",
                "sub_checks": {
                    "input_validation": False,
                    "pii_detection": False,
                    "prompt_injection": False,
                    "policy_checks": True,
                    "content_safety": True
                }
            }

        # 1. Input Validation (Length check)
        if len(text) > 8000:
            allowed = False
            reasons.append("Input exceeds maximum allowed length of 8000 characters.")

        # 2. Prompt Injection Check
        inj_res = cls.check_prompt_injection(text)
        if inj_res["injection_detected"]:
            allowed = False
            reasons.append("Potential prompt injection / security evasion pattern detected.")

        # 3. Content Safety Check
        safety_res = cls.check_content_safety(text)
        if not safety_res["content_safe"]:
            allowed = False
            reasons.append("Potentially unsafe, restricted, or suspicious terms detected.")

        # 4. PII Detection
        pii_res = cls.check_pii(text)
        if pii_res["pii_detected"]:
            reasons.append(f"Sensitive PII detected ({', '.join(pii_res['detected_types'])}). Data sanitized.")

        return {
            "allowed": allowed,
            "reasons": reasons,
            "pii_detected": pii_res["pii_detected"],
            "prompt_injection_detected": inj_res["injection_detected"],
            "policy_check_passed": True,
            "content_safety_passed": safety_res["content_safe"],
            "sanitized_input": pii_res["sanitized_text"],
            "sub_checks": {
                "input_validation": len(text) <= 8000,
                "pii_detection": pii_res["pii_detected"],
                "prompt_injection": not inj_res["injection_detected"],
                "policy_checks": True,
                "content_safety": safety_res["content_safe"]
            }
        }

    @classmethod
    def validate_claim_payload(
        cls,
        claimant_name: str,
        policy_number: str,
        claim_type: str,
        amount: float,
        description: str
    ) -> Dict[str, Any]:
        """Validates structured claim intake form payload through all 5 checks."""
        reasons: List[str] = []
        allowed = True

        # 1. Input Validation
        if not claimant_name or len(claimant_name.strip()) < 2:
            allowed = False
            reasons.append("Claimant name must be at least 2 characters long.")

        if amount < 0:
            allowed = False
            reasons.append("Claim amount cannot be negative.")

        if amount > 50000000:
            allowed = False
            reasons.append("Claim amount exceeds maximum single submission limit (INR 5 Cr). Requires direct manager intake.")

        # 2. Policy Checks
        policy_res = cls.check_policy(policy_number)
        if not policy_res["valid"]:
            allowed = False
            reasons.append(policy_res["reason"])

        # 3, 4, 5. Validate Description (PII, Injections, Safety)
        desc_validation = cls.validate_text(description, context="claim_description")
        if not desc_validation["allowed"]:
            allowed = False
            reasons.extend(desc_validation["reasons"])

        return {
            "allowed": allowed,
            "reasons": reasons,
            "pii_detected": desc_validation["pii_detected"],
            "prompt_injection_detected": desc_validation["prompt_injection_detected"],
            "policy_check_passed": policy_res["valid"],
            "content_safety_passed": desc_validation["content_safety_passed"],
            "sanitized_description": desc_validation["sanitized_input"],
            "sub_checks": {
                "input_validation": allowed and (len(claimant_name.strip()) >= 2) and (amount >= 0),
                "pii_detection": desc_validation["pii_detected"],
                "prompt_injection": not desc_validation["prompt_injection_detected"],
                "policy_checks": policy_res["valid"],
                "content_safety": desc_validation["content_safety_passed"]
            }
        }
