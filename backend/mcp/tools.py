"""
Layer 5: Tools & Integrations Layer (via MCP)
Provides secure access to 10 Enterprise System categories:
1. Policy Management System (API)
2. Claims Database (API) & GNOTHEIA Polycontexts
3. Customer Information System (CRM)
4. Fraud Detection Service (Fraud Bureau)
5. Enterprise Systems (ERP, CRM, HR, ITSM)
6. Productivity Tools (Docs, Sheets, Office export)
7. Web & External APIs (Search, Payments, Maps)
8. File & Document Processing (PDF, Images OCR)
9. RPA / Automation (Payout & Task triggers)
10. Custom Tools (MCP / Open Standards)
"""
from typing import Dict, Any, List, Optional
import os
import datetime
from backend.core.logging_config import logger

# Controlled Demo Policy Database
MOCK_POLICIES: Dict[str, Dict[str, Any]] = {
    "POL-HEALTH-GOLD-2026": {
        "policy_number": "POL-HEALTH-GOLD-2026",
        "policyholder_name": "Mahesh Sharma",
        "type": "Health",
        "sum_insured": 500000.0,
        "status": "Active",
        "start_date": "2024-01-01",
        "end_date": "2027-01-01",
        "copay_percent": 10.0,
        "deductible": 5000.0,
        "network_hospitals_only": False,
        "waiting_period_ped_months": 24
    },
    "POL-MOTOR-COMP-2026": {
        "policy_number": "POL-MOTOR-COMP-2026",
        "policyholder_name": "Priya Patel",
        "type": "Motor",
        "sum_insured": 850000.0,
        "status": "Active",
        "vehicle_reg": "DL-01-AB-1234",
        "idv": 750000.0,
        "zero_depreciation": False,
        "start_date": "2025-05-10",
        "end_date": "2026-05-09"
    },
    "POL-TRAVEL-SHIELD-2026": {
        "policy_number": "POL-TRAVEL-SHIELD-2026",
        "policyholder_name": "Ananya Roy",
        "type": "Travel",
        "sum_insured": 1000000.0,
        "status": "Active",
        "geography": "Worldwide Excl. US/Canada",
        "start_date": "2026-08-01",
        "end_date": "2026-10-30"
    }
}

# Controlled Demo Claims Database
MOCK_CLAIMS: Dict[str, Dict[str, Any]] = {
    "CLM-20260918-A12F": {
        "claim_id": "CLM-20260918-A12F",
        "policy_number": "POL-HEALTH-GOLD-2026",
        "claimant_name": "Mahesh Sharma",
        "type": "Health",
        "amount": 125000.0,
        "incident_date": "2026-09-10",
        "hospital_name": "Apollo Multispeciality Hospital",
        "diagnosis": "Acute Appendicitis with laparoscopic appendectomy",
        "status": "Under Assessment",
        "prior_claims_count": 0
    },
    "CLM-20260918-B81C": {
        "claim_id": "CLM-20260918-B81C",
        "policy_number": "POL-MOTOR-COMP-2026",
        "claimant_name": "Priya Patel",
        "type": "Motor",
        "amount": 82500.0,
        "incident_date": "2026-09-15",
        "garage_name": "Apex Auto Workshop",
        "status": "Risk Review",
        "prior_claims_count": 2
    }
}

# Controlled Demo Customers
MOCK_CUSTOMERS: Dict[str, Dict[str, Any]] = {
    "CUST-001": {
        "customer_id": "CUST-001",
        "name": "Mahesh Sharma",
        "email": "mahesh@example.com",
        "phone": "+91-9876543210",
        "loyalty_tier": "Platinum",
        "risk_tier": "Low Risk",
        "tenure_years": 4
    },
    "CUST-002": {
        "customer_id": "CUST-002",
        "name": "Priya Patel",
        "email": "priya@example.com",
        "phone": "+91-9811122233",
        "loyalty_tier": "Gold",
        "risk_tier": "Medium Risk",
        "tenure_years": 1
    }
}


class MCPToolRegistry:
    """Registry of standard enterprise MCP tools matching all 10 architecture categories."""

    # 1. Policy Management System (API)
    @staticmethod
    def get_policy_details(policy_number: str) -> Dict[str, Any]:
        """Retrieves policy record, active limits, and co-payment terms from Core Insurance Database."""
        logger.info(f"[MCP Tool 1/10] get_policy_details for {policy_number}")
        clean_num = policy_number.strip().upper()
        if clean_num in MOCK_POLICIES:
            return {"success": True, "is_mock": True, "category": "Policy Management System (API)", "data": MOCK_POLICIES[clean_num]}
        return {
            "success": True,
            "is_mock": True,
            "category": "Policy Management System (API)",
            "data": {
                "policy_number": clean_num,
                "type": "General / Health",
                "status": "Active",
                "sum_insured": 500000.0,
                "deductible": 5000.0,
                "copay_percent": 10.0,
                "note": "Standard demo policy parameters inferred."
            }
        }

    # 2. Claims Database (API) with GNOTHEIA Parquet Integration
    @staticmethod
    def get_claim_details(claim_id: str) -> Dict[str, Any]:
        """Fetches historical details and incident data for a claim from Claims Database."""
        logger.info(f"[MCP Tool 2/10] get_claim_details for {claim_id}")
        clean_id = claim_id.strip().upper()
        if clean_id in MOCK_CLAIMS:
            return {"success": True, "is_mock": True, "category": "Claims Database (API)", "data": MOCK_CLAIMS[clean_id]}
        
        # Check GNOTHEIA Parquet repository if available
        gnotheia_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "claims", "GNOTHEIA", "data.parquet")
        if os.path.exists(gnotheia_path):
            try:
                import pandas as pd
                df = pd.read_parquet(gnotheia_path)
                match = df[df['id'].astype(str).str.upper() == clean_id]
                if not match.empty:
                    rec = match.iloc[0].to_dict()
                    return {
                        "success": True,
                        "is_mock": False,
                        "source": "GNOTHEIA Enterprise Dataset",
                        "category": "Claims Database (API)",
                        "data": {
                            "claim_id": str(rec.get("id")),
                            "note": str(rec.get("note", "")),
                            "polycontext_summary": "OMG SBVR Rule-Compliant Polycontext Record",
                            "status": "Ingested Polycontext"
                        }
                    }
            except Exception as e:
                logger.warning(f"[MCP Tool] GNOTHEIA lookup notice: {e}")

        return {"success": False, "is_mock": True, "category": "Claims Database (API)", "error": f"Claim {claim_id} not found in historical repository."}

    # 3. Customer Information System (CRM)
    @staticmethod
    def get_customer_details(customer_id: str) -> Dict[str, Any]:
        """Fetches policyholder profile and tenure from Enterprise CRM."""
        logger.info(f"[MCP Tool 3/10] get_customer_details for {customer_id}")
        clean_id = customer_id.strip().upper()
        if clean_id in MOCK_CUSTOMERS:
            return {"success": True, "is_mock": True, "category": "Customer Information System", "data": MOCK_CUSTOMERS[clean_id]}
        return {"success": False, "is_mock": True, "category": "Customer Information System", "error": f"Customer ID {customer_id} not found."}

    # 4. Fraud Detection Service
    @staticmethod
    def get_risk_indicators(claim_id: str) -> Dict[str, Any]:
        """Retrieves fraud risk indicators, frequency anomalies, and address matching scores."""
        logger.info(f"[MCP Tool 4/10] get_risk_indicators for {claim_id}")
        clean_id = claim_id.strip().upper()
        if clean_id == "CLM-20260918-B81C":
            return {
                "success": True,
                "is_mock": True,
                "category": "Fraud Detection Service",
                "risk_score": 0.68,
                "risk_category": "Requires Investigation",
                "indicators": [
                    "Claim filed within 14 days of policy inception.",
                    "Multiple prior claims recorded across different insurers in past 12 months.",
                    "Workshop flagged for estimate discrepancies."
                ]
            }
        return {
            "success": True,
            "is_mock": True,
            "category": "Fraud Detection Service",
            "risk_score": 0.12,
            "risk_category": "Low Risk",
            "indicators": [
                "Zero prior claims in current policy period.",
                "Accredited network provider verified.",
                "Consistent documentation matches claim timeline."
            ]
        }

    # 5. Enterprise Systems (ERP, CRM, HR, ITSM)
    @staticmethod
    def query_enterprise_erp(module: str, query_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Queries SAP/Oracle ERP, Workday HR, or ServiceNow ITSM for enterprise validation."""
        logger.info(f"[MCP Tool 5/10] query_enterprise_erp for module={module}")
        return {
            "success": True,
            "category": "Enterprise Systems (ERP, CRM, HR, ITSM)",
            "module": module,
            "status": "Synced",
            "active_gl_account": "GL-CLAIMS-2026-SETTLE",
            "reserve_balance_inr": 25000000.0,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    # 6. Productivity Tools (Docs, Sheets, Office)
    @staticmethod
    def export_claim_spreadsheet(claim_id: str, assessment_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generates itemized claim spreadsheet and settlement summary document."""
        logger.info(f"[MCP Tool 6/10] export_claim_spreadsheet for {claim_id}")
        return {
            "success": True,
            "category": "Productivity Tools (Docs, Sheets, Office)",
            "document_name": f"Settlement_Statement_{claim_id}.xlsx",
            "format": "OpenXML Spreadsheet",
            "download_uri": f"/api/v1/documents/export/{claim_id}",
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    # 7. Web & External APIs (Search, Payments, Maps)
    @staticmethod
    def verify_hospital_and_payment_rails(provider_name: str, bank_ifsc: Optional[str] = None) -> Dict[str, Any]:
        """Validates healthcare provider accreditation geolocation and bank routing rails."""
        logger.info(f"[MCP Tool 7/10] verify_hospital_and_payment_rails for {provider_name}")
        return {
            "success": True,
            "category": "Web & External APIs (Search, Payments, Maps)",
            "provider": provider_name,
            "rohil_registry_id": "ROHINI-DEL-8941",
            "geo_coordinates": {"lat": 28.5672, "lng": 77.2100},
            "payout_rails": {"imps_available": True, "neft_available": True, "upi_gateway": "Active"}
        }

    # 8. File & Document Processing (PDF, Images OCR)
    @staticmethod
    def execute_advanced_ocr(filename: str, file_type: str) -> Dict[str, Any]:
        """Applies intelligent computer vision OCR and table structure extraction."""
        logger.info(f"[MCP Tool 8/10] execute_advanced_ocr for {filename}")
        return {
            "success": True,
            "category": "File & Document Processing (PDF, Images)",
            "filename": filename,
            "ocr_engine": "InsurAgent Vision-OCR Engine v2.4",
            "confidence": 0.98,
            "tables_extracted": 1,
            "signatures_detected": True
        }

    # 9. RPA / Automation
    @staticmethod
    def trigger_rpa_payout(claim_id: str, amount: float, beneficiary_account: str) -> Dict[str, Any]:
        """Triggers robotic process automation bot for straight-through payout processing."""
        logger.info(f"[MCP Tool 9/10] trigger_rpa_payout for {claim_id}: amount={amount}")
        return {
            "success": True,
            "category": "RPA / Automation",
            "task_id": f"RPA-TASK-{datetime.datetime.now():%Y%m%d}-{claim_id[-4:]}",
            "amount_authorized": amount,
            "status": "Queued for automated core-banking disbursement",
            "estimated_disbursement_time_mins": 2
        }

    # 10. Custom Tools (MCP / Open Standards) & Notifications
    @staticmethod
    def send_notification(recipient: str, message: str) -> Dict[str, Any]:
        """Dispatches SMS/Email/WhatsApp notification or adjuster task assignment via open MCP standard."""
        logger.info(f"[MCP Tool 10/10] send_notification to {recipient}")
        return {
            "success": True,
            "category": "Custom Tools (MCP / Open Standards)",
            "recipient": recipient,
            "status": "Dispatched",
            "channel": "Enterprise Multi-Channel Gateway (Email/WhatsApp/SMS)",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
