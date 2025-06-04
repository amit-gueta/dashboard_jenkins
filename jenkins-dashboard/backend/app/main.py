from fastapi import FastAPI
from app.core.config import settings
# from app.api import builds, analytics # Will be uncommented later
# from app.db.session import engine # Will be uncommented later
# from app.db import base # Will be uncommented later

# base.Base.metadata.create_all(bind=engine) # Create tables - consider using Alembic for migrations

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# app.include_router(builds.router, prefix="/api/builds", tags=["builds"])
# app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

# Placeholder for Celery app (if needed directly in main)
# from app.core.celery_app import celery_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
