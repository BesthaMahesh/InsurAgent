"""
MCP Client for agents to invoke registered tools across all 10 architecture categories.
"""
from typing import Dict, Any, Optional
from backend.mcp.server import mcp_server
from backend.core.logging_config import logger


class MCPClient:
    """Client for executing MCP enterprise integration tools."""

    def __init__(self, server=None):
        self.server = server or mcp_server

    def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Invokes a tool on the MCP server."""
        args = arguments or {}
        logger.info(f"[MCP Client] Calling tool '{tool_name}' with args {args}")
        return self.server.execute_tool(tool_name, args)

    def list_available_tools(self) -> Dict[str, Any]:
        return self.server.list_tools()

    # 1. Policy Management System (API)
    def get_policy_details(self, policy_number: str) -> Dict[str, Any]:
        return self.call_tool("get_policy_details", {"policy_number": policy_number})

    # 2. Claims Database (API)
    def get_claim_details(self, claim_id: str) -> Dict[str, Any]:
        return self.call_tool("get_claim_details", {"claim_id": claim_id})

    # 3. Customer Information System
    def get_customer_details(self, customer_id: str) -> Dict[str, Any]:
        return self.call_tool("get_customer_details", {"customer_id": customer_id})

    # 4. Fraud Detection Service
    def get_risk_indicators(self, claim_id: str) -> Dict[str, Any]:
        return self.call_tool("get_risk_indicators", {"claim_id": claim_id})

    # 5. Enterprise Systems (ERP, CRM, HR, ITSM)
    def query_enterprise_erp(self, module: str = "claims_reserve") -> Dict[str, Any]:
        return self.call_tool("query_enterprise_erp", {"module": module})

    # 6. Productivity Tools (Docs, Sheets, Office)
    def export_claim_spreadsheet(self, claim_id: str) -> Dict[str, Any]:
        return self.call_tool("export_claim_spreadsheet", {"claim_id": claim_id})

    # 7. Web & External APIs (Search, Payments, Maps)
    def verify_hospital_and_payment_rails(self, provider_name: str) -> Dict[str, Any]:
        return self.call_tool("verify_hospital_and_payment_rails", {"provider_name": provider_name})

    # 8. File & Document Processing (PDF, Images)
    def execute_advanced_ocr(self, filename: str, file_type: str = "pdf") -> Dict[str, Any]:
        return self.call_tool("execute_advanced_ocr", {"filename": filename, "file_type": file_type})

    # 9. RPA / Automation
    def trigger_rpa_payout(self, claim_id: str, amount: float, beneficiary_account: str = "BEN-AUTO-9988") -> Dict[str, Any]:
        return self.call_tool("trigger_rpa_payout", {"claim_id": claim_id, "amount": amount, "beneficiary_account": beneficiary_account})

    # 10. Custom Tools (MCP / Open Standards)
    def send_notification(self, recipient: str, message: str) -> Dict[str, Any]:
        return self.call_tool("send_notification", {"recipient": recipient, "message": message})
