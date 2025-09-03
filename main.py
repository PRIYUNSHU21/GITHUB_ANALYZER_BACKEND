import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.github_routes import router as github_router
from config.settings import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="A comprehensive GitHub repository analyzer with AI-powered insights"
)

# Add CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(github_router)

@app.get("/")
async def root():
    return {
        "message": "GitHub Repository Analyzer API",
        "version": settings.VERSION,
        "docs": "/docs",
        "status": "deployed"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.DEBUG
    )
