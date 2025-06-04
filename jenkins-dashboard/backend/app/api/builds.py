from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import session
from app.schemas import build as build_schema
# from app.services import build_service # Placeholder

router = APIRouter()

@router.get("/{project}", response_model=List[build_schema.Build])
def list_project_builds(project: str, db: Session = Depends(session.get_db), skip: int = 0, limit: int = 100):
    # builds = build_service.get_builds_by_project(db, project=project, skip=skip, limit=limit)
    # return builds
    return [] # Placeholder

@router.get("/{project}/{mr}/{build_num}", response_model=build_schema.Build) # Corrected build_num to build_num
def get_build_details(project: str, mr: str, build_num: int, db: Session = Depends(session.get_db)):
    # build = build_service.get_build(db, project=project, mr_number=mr, build_number=build_num)
    # if build is None:
    #     raise HTTPException(status_code=404, detail="Build not found")
    # return build
    raise HTTPException(status_code=404, detail="Build not found") # Placeholder

@router.post("/sync", status_code=202)
async def trigger_manual_sync(sync_request: build_schema.BuildSyncRequest):
    # Trigger a background task for syncing
    # For now, just a placeholder response
    return {"message": "Sync job accepted", "project": sync_request.project, "full_sync": sync_request.full_sync}

@router.get("/projects", response_model=List[str]) # Added /projects endpoint
def list_available_projects(db: Session = Depends(session.get_db)):
    # projects = build_service.get_distinct_projects(db)
    # return projects
    return [] # Placeholder
