"""
MCP Server handler simulating Model Context Protocol tool calling server across all 10 architecture categories.
"""
from typing import Dict, Any
from backend.mcp.tools import MCPToolRegistry
from backend.core.logging_config import logger


class MCPServer:
    """Enterprise MCP Server providing standard tool execution interface."""

    def __init__(self):
        self.tools = {
            # 1. Policy Management System (API)
            "get_policy_details": MCPToolRegistry.get_policy_details,
            # 2. Claims Database (API)
            "get_claim_details": MCPToolRegistry.get_claim_details,
            # 3. Customer Information System
            "get_customer_details": MCPToolRegistry.get_customer_details,
            # 4. Fraud Detection Service
            "get_risk_indicators": MCPToolRegistry.get_risk_indicators,
            # 5. Enterprise Systems (ERP, CRM, HR, ITSM)
            "query_enterprise_erp": MCPToolRegistry.query_enterprise_erp,
            # 6. Productivity Tools (Docs, Sheets, Office)
            "export_claim_spreadsheet": MCPToolRegistry.export_claim_spreadsheet,
            # 7. Web & External APIs (Search, Payments, Maps)
            "verify_hospital_and_payment_rails": MCPToolRegistry.verify_hospital_and_payment_rails,
            # 8. File & Document Processing (PDF, Images OCR)
            "execute_advanced_ocr": MCPToolRegistry.execute_advanced_ocr,
            # 9. RPA / Automation
            "trigger_rpa_payout": MCPToolRegistry.trigger_rpa_payout,
            # 10. Custom Tools (MCP / Open Standards)
            "send_notification": MCPToolRegistry.send_notification
        }

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches tool call to appropriate handler."""
        if tool_name not in self.tools:
            logger.warning(f"MCP tool '{tool_name}' not registered.")
            return {"success": False, "error": f"Tool '{tool_name}' not found."}
        
        handler = self.tools[tool_name]
        try:
            return handler(**arguments)
        except TypeError as e:
            logger.error(f"Invalid arguments for tool '{tool_name}': {e}")
            return {"success": False, "error": f"Invalid arguments: {str(e)}"}
        except Exception as e:
            logger.error(f"Error executing MCP tool '{tool_name}': {e}")
            return {"success": False, "error": str(e)}

    def list_tools(self) -> Dict[str, Any]:
        """Returns catalog of registered 10 MCP tools."""
        return {
            "tools": [
                {
                    "name": "get_policy_details",
                    "category": "1. Policy Management System (API)",
                    "description": "Retrieve policy coverage, deductible, and limit details.",
                    "inputSchema": {"type": "object", "properties": {"policy_number": {"type": "string"}}, "required": ["policy_number"]}
                },
                {
                    "name": "get_claim_details",
                    "category": "2. Claims Database (API)",
                    "description": "Fetch claim incident record and GNOTHEIA polycontexts.",
                    "inputSchema": {"type": "object", "properties": {"claim_id": {"type": "string"}}, "required": ["claim_id"]}
                },
                {
                    "name": "get_customer_details",
                    "category": "3. Customer Information System",
                    "description": "Fetch policyholder CRM profile.",
                    "inputSchema": {"type": "object", "properties": {"customer_id": {"type": "string"}}, "required": ["customer_id"]}
                },
                {
                    "name": "get_risk_indicators",
                    "category": "4. Fraud Detection Service",
                    "description": "Query insurance fraud and risk bureau indicators.",
                    "inputSchema": {"type": "object", "properties": {"claim_id": {"type": "string"}}, "required": ["claim_id"]}
                },
                {
                    "name": "query_enterprise_erp",
                    "category": "5. Enterprise Systems (ERP, CRM, HR, ITSM)",
                    "description": "Query SAP/Oracle ERP claims ledger balance and reserves.",
                    "inputSchema": {"type": "object", "properties": {"module": {"type": "string"}}, "required": ["module"]}
                },
                {
                    "name": "export_claim_spreadsheet",
                    "category": "6. Productivity Tools (Docs, Sheets, Office)",
                    "description": "Export itemized claim settlement sheet in OpenXML format.",
                    "inputSchema": {"type": "object", "properties": {"claim_id": {"type": "string"}}, "required": ["claim_id"]}
                },
                {
                    "name": "verify_hospital_and_payment_rails",
                    "category": "7. Web & External APIs (Search, Payments, Maps)",
                    "description": "Validate provider geolocation and banking rails.",
                    "inputSchema": {"type": "object", "properties": {"provider_name": {"type": "string"}}, "required": ["provider_name"]}
                },
                {
                    "name": "execute_advanced_ocr",
                    "category": "8. File & Document Processing (PDF, Images)",
                    "description": "Extract text, invoice tables, and signatures via OCR.",
                    "inputSchema": {"type": "object", "properties": {"filename": {"type": "string"}, "file_type": {"type": "string"}}, "required": ["filename", "file_type"]}
                },
                {
                    "name": "trigger_rpa_payout",
                    "category": "9. RPA / Automation",
                    "description": "Trigger robotic automated straight-through payout disbursement.",
                    "inputSchema": {"type": "object", "properties": {"claim_id": {"type": "string"}, "amount": {"type": "number"}, "beneficiary_account": {"type": "string"}}, "required": ["claim_id", "amount", "beneficiary_account"]}
                },
                {
                    "name": "send_notification",
                    "category": "10. Custom Tools (MCP / Open Standards)",
                    "description": "Dispatch notification to customer or adjuster.",
                    "inputSchema": {"type": "object", "properties": {"recipient": {"type": "string"}, "message": {"type": "string"}}, "required": ["recipient", "message"]}
                }
            ]
        }


mcp_server = MCPServer()
