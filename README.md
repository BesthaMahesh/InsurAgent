# 🛡️ InsurAgent — Enterprise Multi-Agent Claim Processing & Audit System

> **Enterprise Multi-Agent Claims Intelligence Platform**  
> AI-assisted claim adjudication, grounded policy verification (RAG), external tool calling (MCP), deterministic guardrails, and immutable auditability.

---

## 1. Project Overview
**InsurAgent** is a multi-agent AI claims adjudication and audit platform built for health, motor, and travel insurance lines. It coordinates specialized autonomous agents orchestrated through **LangGraph** to intake, verify, analyze risk, evaluate coverage, synthesize adjudication recommendations, and produce an immutable regulatory audit trail.

---

## 2. Business Problem
Traditional insurance claims processing faces critical operational challenges:
- **Lengthy Turnaround Times**: Adjudicators manually cross-reference 50+ page policy wordings and invoices.
- **Inconsistent Decision-Making**: Discrepancies between adjusters regarding exclusions, waiting periods, and deductibles.
- **Opaque Audit Trails**: Lack of granular step-by-step reasoning behind automated decisions creates regulatory compliance hurdles.
- **Risk & Fraud Vulnerability**: Anomaly indicators get overlooked during high-volume periods.

---

## 3. What InsurAgent Solves
InsurAgent empowers claim analysts with:
1. **Automated Evidence Extraction**: Ingests and summarizes itemized bills, discharge summaries, and estimates.
2. **Grounded Policy Verification (RAG)**: Retrieves exact policy clauses from vector storage and prevents hallucinated rules.
3. **Multi-Agent Collaboration**: Specialized agents divide responsibilities (Intake, Document Intelligence, Policy RAG, Risk Analysis, Assessment Synthesis, and Audit).
4. **Deterministic Guardrails**: Filters PII, blocks prompt injections, and enforces strict compliance boundaries.
5. **Responsible Human-in-the-Loop (HITL)**: Flags high-risk or low-confidence claims for mandatory adjuster review.

---

## 4. Architecture

```
                                  [ Claimant / Adjuster ]
                                             │
                                             ▼
                             [ Streamlit Interactive Frontend ]
                                             │
                                   (HTTP REST / JSON)
                                             │
                                             ▼
                                [ FastAPI Backend Gateway ]
                                             │
                                   [ Input Guardrail ]
                      (PII Redaction, Prompt Injection Defense, Validation)
                                             │
                                             ▼
                     ╔═══════════════════════════════════════════════╗
                     ║         LangGraph Multi-Agent Engine          ║
                     ║                                               ║
                     ║   [ Supervisor / Router Agent ]               ║
                     ║                 │                             ║
                     ║   [ Claim Intake Agent ]                      ║
                     ║                 │                             ║
                     ║   [ Document Analysis Agent ]                 ║
                     ║                 │                             ║
                     ║   [ Policy Verification Agent (RAG) ] ◄──┐    ║
                     ║                 │                        │    ║
                     ║   [ Fraud / Risk Agent (MCP Tools) ] ◄─┐ │    ║
                     ║                 │                      │ │    ║
                     ║   [ Claim Assessment Agent ]           │ │    ║
                     ║                 │                      │ │    ║
                     ║   [ Human-in-the-Loop Router ]         │ │    ║
                     ║                 │                      │ │    ║
                     ║   [ Audit & Compliance Agent ]         │ │    ║
                     ╚═════════════════╤══════════════════════╪═╪════╝
                                       │                      │ │
                        ┌──────────────┴──────────────┐       │ │
                        ▼                             ▼       │ │
            [ Output Safety Guardrail ]   [ Persistent Store ]│ │
            (Grounding, Explainability)   (SQLite & Audit DB) │ │
                        │                                     │ │
                        ▼                                     │ │
            [ Structured Response ]                           │ │
                                                              │ │
    ┌─────────────────────────────────────────────────────────┼─┘
    │  RAG Knowledge Layer (ChromaDB Vector Store)            │
    │  - data/policies/  - data/guidelines/  - data/compliance│
    │                                                         │
    └─────────────────────────────────────────────────────────┼─┐
                                                              │ │
    ┌─────────────────────────────────────────────────────────┴─┘
    │  MCP External Tools (Model Context Protocol)
    │  - get_policy_details  - get_risk_indicators  - send_notification
    └───────────────────────────────────────────────────────────
```

---

## 5. Multi-Agent Workflow
The LangGraph pipeline runs sequentially with conditional escalation routing:

1. **Input Guardrail**: Validates inputs, detects & masks sensitive PII (credit cards, national IDs), and blocks prompt injection attempts.
2. **Supervisor / Router Agent**: Directs state and execution route.
3. **Claim Intake Agent**: Normalizes claimant data and standardizes claim types.
4. **Document Analysis Agent**: Extracts text and metadata from PDF bills and receipts.
5. **Policy Verification Agent**: Retrieves exact policy clauses via RAG and strictly grounds coverage decisions.
6. **Fraud / Risk Agent**: Calculates risk score (Low, Medium, High, Requires Investigation) and checks MCP bureau indicators.
7. **Claim Assessment Agent**: Synthesizes coverage, deductibles, and risk into an adjudication recommendation.
8. **Human Review Router**: Conditionally routes to Human Review if risk score $\ge 0.60$, confidence $< 0.75$, or required documents are missing.
9. **Audit & Compliance Agent**: Records immutable audit events into SQLite.
10. **Output Guardrail**: Sanitizes output against data leaks and ensures compliance disclaimers are attached.

---

## 6. RAG (Retrieval-Augmented Generation)
- **Vector Database**: ChromaDB (`data/chromadb`).
- **Grounded Verification**: The retriever queries chunked policy documents and returns source metadata (document, section, similarity score).
- **Anti-Hallucination Policy**: If retrieval returns no matching clauses, the agent explicitly emits `No relevant policy information found` without fabricating clauses.

---

## 7. MCP (Model Context Protocol)
Implements enterprise tool calling via standard MCP architecture:
- `get_policy_details(policy_number)`: Retrieves core policy limits and deductibles.
- `get_claim_details(claim_id)`: Fetches historical claim records.
- `get_customer_details(customer_id)`: Queries CRM profiles.
- `get_risk_indicators(claim_id)`: Checks fraud bureau anomaly indicators.
- `send_notification(recipient, message)`: Dispatches alerts and notifications.

*Note: In development mode, these integrate with controlled demo enterprise data.*

---

## 8. Guardrails
- **Input Guardrails**:
  - Deterministic regex checking for Prompt Injections (e.g. instruction override, system prompt extraction, jailbreaks).
  - PII Detection & Redaction (`[CARD_REDACTED]`, `[ID_REDACTED]`).
  - Boundary limits on text size and numeric claims.
- **Output Guardrails**:
  - Output sanitization preventing reflected sensitive data.
  - Mandatory disclaimer insertion indicating AI-assisted decision support.
  - Confidence and grounding compliance triggers.

---

## 9. Human-in-the-Loop (HITL)
InsurAgent never makes uncontrolled final claim rejections or approvals.
A case is flagged with `requires_human_review = True` and escalated when:
- Risk score exceeds high-risk threshold ($\ge 0.60$).
- Claim confidence is below threshold ($< 0.75$).
- Mandatory supporting documentation is missing.
- Grounded policy evidence is unverified in knowledge base.

---

## 10. Auditability
Every stage of processing logs structured events to SQLite:
- `timestamp`: UTC timestamp.
- `claim_id`: Associated claim.
- `agent`: Executing agent module.
- `action`: Specific decision or step.
- `source`: Knowledge doc or MCP tool reference.
- `status`: `success`, `blocked`, or `review_required`.

---

## 11. Responsible AI
Cross-cutting governance controls:
- **Privacy**: PII masking in logs and outputs.
- **Explainability**: Plain-language reasoning with cited policy clauses.
- **Accountability**: Immutable audit trail for every action.
- **Security**: No hard-coded secrets, environment-driven configuration.
- **Fairness & Safety**: Deterministic safety checks without reliance on ungrounded LLM decisions.

---

## 12. Technology Stack
- **Frontend**: Streamlit
- **Backend API**: FastAPI, Uvicorn, Pydantic v2
- **Agent Orchestration**: LangGraph, LangChain
- **LLM Provider**: Groq Cloud (`llama-3.3-70b-versatile` / configurable)
- **Vector Database**: ChromaDB
- **Database**: SQLite / SQLAlchemy
- **Testing**: Pytest, HTTPX

---

## 13. Project Structure

```
InsurAgent/
├── app.py                         # Streamlit Frontend
├── requirements.txt               # Pinned dependencies
├── .env.example                   # Environment template
├── .env                           # Active environment configuration
├── Dockerfile                     # Container definition
├── docker-compose.yml             # Multi-service container orchestration
│
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── client.py                  # Frontend-to-Backend HTTP client
│   ├── api/
│   │   ├── routes_claims.py       # POST /api/claims/process, GET /api/claims/{id}
│   │   ├── routes_chat.py         # POST /api/chat (Ask InsurAgent)
│   │   ├── routes_audit.py        # GET /api/audit/{claim_id}
│   │   └── routes_health.py       # GET /api/health
│   ├── agents/
│   │   ├── supervisor_agent.py    # Orchestration & planning
│   │   ├── claim_intake_agent.py  # Validation & normalization
│   │   ├── document_agent.py      # PDF & invoice parsing
│   │   ├── policy_agent.py        # RAG policy grounding
│   │   ├── risk_agent.py          # Fraud & anomaly analysis
│   │   ├── assessment_agent.py    # Synthesis & recommendation
│   │   └── audit_agent.py         # Audit trail recording
│   ├── graph/
│   │   ├── state.py               # Typed AgentState
│   │   ├── nodes.py               # Graph execution nodes
│   │   └── workflow.py            # LangGraph StateGraph & conditional routing
│   ├── guardrails/
│   │   ├── input_guardrail.py     # Deterministic safety & PII filter
│   │   └── output_guardrail.py    # Grounding & redaction filter
│   ├── rag/
│   │   ├── vectorstore.py         # ChromaDB client
│   │   ├── ingest.py              # Knowledge ingestion script
│   │   └── retriever.py           # Top-K grounded retriever
│   ├── mcp/
│   │   ├── server.py              # Mock MCP server
│   │   ├── client.py              # MCP tool client
│   │   └── tools.py               # Enterprise tool definitions
│   ├── services/
│   │   ├── claim_service.py       # Claims database CRUD
│   │   ├── document_service.py    # PDF and text extraction
│   │   └── audit_service.py       # Audit logging service
│   ├── models/
│   │   ├── claim.py               # ClaimRequest, ClaimDetails schemas
│   │   └── response.py            # ClaimResponse, ChatResponse schemas
│   ├── core/
│   │   ├── config.py              # Pydantic Settings
│   │   ├── logging_config.py      # PII-masking logger
│   │   └── llm.py                 # LLM factory
│   └── database/
│       └── database.py            # SQLite schema & tables
│
├── data/
│   ├── policies/                  # Demo policy markdown files
│   ├── guidelines/                # Assessment guidelines
│   ├── compliance/                # Regulatory standards
│   └── faq/                       # Insurance FAQs
│
└── tests/
    ├── test_guardrails.py         # Input/Output guardrail tests
    ├── test_rag.py                # Vector search tests
    ├── test_agents.py             # Agent unit tests
    ├── test_graph.py              # LangGraph workflow tests
    └── test_api.py                # FastAPI endpoint tests
```

---

## 14. Installation

```bash
# Clone the repository
cd InsurAgent

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate  # On Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

---

## 15. Environment Variables
Copy `.env.example` to `.env` and set your API keys:

```ini
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
DATABASE_URL=sqlite:///./data/insuragent.db
CHROMA_DB_PATH=./data/chromadb
RAG_TOP_K=4
CONFIDENCE_THRESHOLD=0.75
HIGH_RISK_THRESHOLD=0.60
API_HOST=0.0.0.0
API_PORT=8000
BACKEND_API_URL=http://localhost:8000
```

---

## 16. Running RAG Ingestion
Ingest sample policies into ChromaDB:

```bash
python -m backend.rag.ingest
```

---

## 17. Running the Backend API
Start the FastAPI server:

```bash
python -m backend.main
# Or:
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger UI docs will be available at: `http://localhost:8000/docs`.

---

## 18. Running Streamlit Frontend
Launch the frontend:

```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 19. Running MCP Server
MCP tools are directly accessible through `backend/mcp/server.py` and invoked via `backend/mcp/client.py`.

---

## 20. Running Tests
Run the comprehensive test suite:

```bash
pytest tests/ -v
```

---

## 21. Demo Workflow

### Scenario: Natural Language Grounded Query
In the **Dashboard** under **Ask InsurAgent**, enter:
```
Check whether claim CLM-20260918-A12F is covered under the policy and explain the reason.
```

**Expected Flow & Result:**
- **Input Guardrail**: Verified & clean.
- **Supervisor**: Routes query through RAG & MCP lookup.
- **Policy Knowledge**: Retrieves `health_policy_gold_plus.md` clauses for Inpatient Hospitalization.
- **MCP Lookup**: Retrieves claim `CLM-20260918-A12F` details for Mahesh Sharma (Appendectomy surgery).
- **Assessment**: `Potentially Covered / Under Assessment`.
- **Evidence**: Grounded in Gold Health Policy Section 1.2 (Inpatient hospitalization covered).
- **Audit**: Logged event to SQLite database.

---

## 22. Limitations
- **OCR Engine**: Standard heuristic and text extraction implemented; optical OCR integration (Tesseract/EasyOCR) can be enabled for scanned non-searchable image PDFs.
- **Mock MCP Data**: External PAS (Policy Administration) and Fraud Bureau integrations use controlled demonstration datasets.

---

## 23. Future Improvements
- Multi-modal computer vision for damage photo severity analysis.
- Live webhook integrations with real Core Insurance PAS (Guidewire / Duck Creek).
- Real-time WebSockets streaming for live agent-step telemetry in the frontend.
