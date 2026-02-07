from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.utils.database import init_db, get_db
from app.utils.cache import cache
from app.utils.logger import logger
from app.bot.webhook import router as webhook_router
from sqlalchemy.orm import Session

# Import API routers
from app.api import knowledge, faqs, documents, conversations, test_bot, agents, flows, message_templates, settings as settings_api, auth, chatwoot

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Chatbot inteligente con IA y base de conocimientos",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Avoid automatic redirects for missing/extra trailing slashes
app.router.redirect_slashes = False

# CORS middleware - MUST be added before routes
origins = settings.cors_origins if settings.environment == "production" else ["http://localhost:8080", "http://31.97.91.222:8080", "http://bot.iaclub.pro", "https://bot.iaclub.pro"]

# Fix: allow_credentials cannot be used with allow_origins=["*"]
use_credentials = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=use_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info(f"Starting {settings.app_name}...")
    logger.info(f"Environment: {settings.environment}")
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
    
    # Connect to Redis
    try:
        await cache.connect()
        logger.info("Redis connected")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down...")
    await cache.disconnect()


# Health check
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.app_name,
        "version": "1.0.0",
        "status": "running",
        "environment": settings.environment
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Check database
        db.execute("SELECT 1")
        db_status = "ok"
    except:
        db_status = "error"
    
    return {
        "status": "ok",
        "database": db_status,
        "cache": "ok" if cache.redis_client else "disconnected"
    }


# Include routers
app.include_router(auth.router, tags=["auth"])
app.include_router(webhook_router, tags=["webhook"])
app.include_router(chatwoot.router, prefix="/api/chatwoot", tags=["chatwoot"])
app.include_router(knowledge.router, tags=["knowledge"])
app.include_router(faqs.router, tags=["faqs"])
app.include_router(documents.router, tags=["documents"])
app.include_router(conversations.router, tags=["conversations"])
app.include_router(test_bot.router, tags=["test"])
app.include_router(agents.router, tags=["agents"])
app.include_router(flows.router, tags=["flows"])
app.include_router(message_templates.router, tags=["message-templates"])
app.include_router(settings_api.router, tags=["settings"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
