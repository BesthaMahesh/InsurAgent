from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Base Directory of Project
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """InsurAgent Application Configuration."""

    # LLM Settings
    LLM_PROVIDER: str = Field(default="groq", description="LLM provider name: groq, openai, or mock")
    GROQ_API_KEY: str = Field(default="", description="Groq Cloud API Key")
    MODEL_NAME: str = Field(default="llama-3.3-70b-versatile", description="Model identifier")

    # Database & Storage
    DATABASE_URL: str = Field(default=f"sqlite:///{BASE_DIR}/data/insuragent.db", description="Database URI")
    CHROMA_DB_PATH: str = Field(default=str(BASE_DIR / "data" / "chromadb"), description="Chroma Vectorstore storage path")
    UPLOAD_DIR: str = Field(default=str(BASE_DIR / "data" / "uploads"), description="Temporary document upload directory")

    # Guardrails & Workflow Thresholds
    RAG_TOP_K: int = Field(default=4, description="Number of policy chunks to retrieve")
    CONFIDENCE_THRESHOLD: float = Field(default=0.75, description="Confidence threshold below which human review is requested")
    HIGH_RISK_THRESHOLD: float = Field(default=0.60, description="Risk threshold above which human review is requested")

    # API Server Settings
    API_HOST: str = Field(default="0.0.0.0", description="API host")
    API_PORT: int = Field(default=8000, description="API port")
    BACKEND_API_URL: str = Field(default="http://localhost:8000", description="Backend URL for frontend client")

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

# Ensure directories exist
Path(settings.CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(BASE_DIR / "data").mkdir(parents=True, exist_ok=True)
