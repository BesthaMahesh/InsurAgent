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

# Environment configuration
ENV CHROMA_TELEMETRY_ENABLED="false"
ENV ANONYMIZED_TELEMETRY="False"
ENV PORT=8501

# Expose ports
EXPOSE 8501 8000

# Start Streamlit application
CMD streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0 --server.headless true
