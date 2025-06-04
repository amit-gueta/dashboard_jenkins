from fastapi import FastAPI
from app.core.config import settings # Ensure settings are loaded
from app.api import builds as api_builds_router # Alias for clarity
from app.api import ingress as api_ingress_router # Alias for clarity

# Database table creation using init.sql via Docker Compose is preferred over create_all.
# from app.db.session import engine
# from app.db import base
# base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" # Use API_V1_STR from settings
)

# Health check endpoint
@app.get(f"{settings.API_V1_STR}/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "project_name": settings.PROJECT_NAME}

# Include API routers
app.include_router(api_builds_router.router, prefix=f"{settings.API_V1_STR}/builds", tags=["Builds"])
app.include_router(api_ingress_router.router, prefix=f"{settings.API_V1_STR}/ingress", tags=["Ingress"])

# Main entry point for Uvicorn (if run directly, e.g. python main.py)
if __name__ == "__main__":
    import uvicorn
    # This is mostly for local development if not using the Docker CMD.
    # The Docker CMD directly calls: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
