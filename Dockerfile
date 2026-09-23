# InsurAgent Multi-Agent Claims Intelligence Platform
FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Ingest initial demo policy knowledge
RUN python -m backend.rag.ingest || true

# Expose ports: 8000 for FastAPI backend, 8501 for Streamlit UI
EXPOSE 8000 8501

# Default command starts FastAPI backend
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
