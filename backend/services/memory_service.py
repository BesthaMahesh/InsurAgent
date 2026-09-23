"""
Layer 3: Knowledge & Memory Layer
Provides Episodic Memory (interactions, events), Long-Term Memory (user, org, domain facts),
and Knowledge Graph entity relations for enterprise claim processing.
"""
from typing import Dict, Any, List, Optional
import datetime
from backend.core.logging_config import logger


class MemoryService:
    """
    Enterprise Memory Management Engine.
    Handles Episodic Memory, Long-Term Semantic Memory, and Knowledge Graph associations.
    """

    # In-memory stores for runtime episodic and long-term memory
    _episodic_memory: List[Dict[str, Any]] = []
    _long_term_memory: Dict[str, Dict[str, Any]] = {
        "user:CUST-001": {
            "preferred_communication": "Email",
            "risk_profile": "Low Risk",
            "historical_satisfaction": 4.9,
            "declared_chronic_conditions": ["None"]
        },
        "user:CUST-002": {
            "preferred_communication": "WhatsApp",
            "risk_profile": "Medium Risk",
            "historical_satisfaction": 4.2,
            "declared_chronic_conditions": ["Hypertension"]
        },
        "domain:health_deductibles": {
            "standard_copay_percent": 10.0,
            "default_deductible_inr": 5000.0,
            "tpa_network_tat_hours": 24
        },
        "org:regulatory_mandates": {
            "irdai_tat_days": 30,
            "hipaa_redaction_required": True,
            "gdpr_data_residency": "IN-CENTRAL"
        }
    }

    _knowledge_graph_triples: List[Dict[str, str]] = [
        {"subject": "Health Policy Gold Plus", "predicate": "COVERS", "object": "Inpatient Hospitalization"},
        {"subject": "Health Policy Gold Plus", "predicate": "REQUIRES_WAITING_PERIOD", "object": "Pre-Existing Diseases (24 Months)"},
        {"subject": "Health Policy Gold Plus", "predicate": "EXCLUDES", "object": "Cosmetic Surgeries"},
        {"subject": "Motor Comprehensive Policy", "predicate": "APPLIES_DEPRECIATION", "object": "Plastic/Rubber Parts (50%)"},
        {"subject": "Travel Shield Policy", "predicate": "COVERS", "object": "Trip Cancellation & Medical Evacuation"},
        {"subject": "IRDAI Grievance Standard", "predicate": "MANDATES_RESOLUTION_TAT", "object": "15 Days for Redressal"},
        {"subject": "Apollo Multispeciality Hospital", "predicate": "IS_NETWORK_PROVIDER_FOR", "object": "Cashless Hospitalization"}
    ]

    @classmethod
    def record_episodic_event(cls, claim_id: str, agent: str, action: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Records an interaction event into episodic memory."""
        event = {
            "event_id": f"EPI-{len(cls._episodic_memory) + 1:05d}",
            "claim_id": claim_id,
            "agent": agent,
            "action": action,
            "metadata": metadata or {},
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        cls._episodic_memory.append(event)
        logger.debug(f"[MemoryService] Recorded episodic event for {claim_id}: {action[:50]}")
        return event

    @classmethod
    def get_episodic_history(cls, claim_id: str) -> List[Dict[str, Any]]:
        """Retrieves episodic interaction history for a given claim."""
        return [ev for ev in cls._episodic_memory if ev.get("claim_id") == claim_id]

    @classmethod
    def get_long_term_context(cls, key: str) -> Optional[Dict[str, Any]]:
        """Retrieves domain, org, or user context from long-term memory."""
        return cls._long_term_memory.get(key)

    @classmethod
    def set_long_term_context(cls, key: str, data: Dict[str, Any]) -> None:
        """Stores or updates long-term memory."""
        cls._long_term_memory[key] = {**cls._long_term_memory.get(key, {}), **data}

    @classmethod
    def query_knowledge_graph(cls, query_term: str) -> List[Dict[str, str]]:
        """Searches the knowledge graph for related policy and domain relations."""
        term_lower = query_term.lower()
        matched = []
        for triple in cls._knowledge_graph_triples:
            if (term_lower in triple["subject"].lower() or 
                term_lower in triple["predicate"].lower() or 
                term_lower in triple["object"].lower()):
                matched.append(triple)
        return matched

    @classmethod
    def get_all_graph_triples(cls) -> List[Dict[str, str]]:
        """Returns all knowledge graph triples."""
        return list(cls._knowledge_graph_triples)
