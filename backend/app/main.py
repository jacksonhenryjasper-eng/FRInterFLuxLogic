from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("AI Bridge SaaS starting up...")
    yield
    # Shutdown
    print("AI Bridge SaaS shutting down...")

# Create FastAPI app
app = FastAPI(
    title="AI Bridge SaaS",
    description="Bridge AI assistants to any application",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.routes import auth, integrations, ai, apps

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(integrations.router, prefix="/api/integrations", tags=["Integrations"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Bridge"])
app.include_router(apps.router, prefix="/api/apps", tags=["Applications"])

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": "2026-08-23T00:00:00Z",
        "service": "AI Bridge SaaS"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Bridge SaaS API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)