from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.logging_config import logger
from backend.database.database import init_db
from backend.api.routes_health import router as health_router
from backend.api.routes_claims import router as claims_router
from backend.api.routes_chat import router as chat_router
from backend.api.routes_audit import router as audit_router
from backend.api.routes_governance import router as governance_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info("Starting up InsurAgent Multi-Agent Claims Backend...")
    init_db()
    logger.info("Database and subsystem initialization completed.")
    yield
    logger.info("InsurAgent backend shutdown.")


app = FastAPI(
    title="InsurAgent Backend",
    description="Enterprise Multi-Agent Claims Intelligence & Audit Platform API",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health_router)
app.include_router(claims_router)
app.include_router(chat_router)
app.include_router(audit_router)
app.include_router(governance_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to InsurAgent Multi-Agent Claims API",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
