from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import session as db_session
from app.schemas import build as build_schemas
from app.services import build_service

router = APIRouter()

@router.get("/", response_model=List[build_schemas.Build])
def read_all_builds(
    project: Optional[str] = None,
    db: Session = Depends(db_session.get_db),
    skip: int = 0,
    limit: int = 100
):
    # Retrieve all builds, optionally filtered by project. Includes stages.
    if project:
        builds = build_service.get_builds_by_project(db, project=project, skip=skip, limit=limit)
    else:
        builds = build_service.get_all_builds(db, skip=skip, limit=limit)
    return builds

@router.get("/projects", response_model=List[str])
def read_distinct_projects(db: Session = Depends(db_session.get_db)):
    # Retrieve a list of unique project names.
    return build_service.get_distinct_projects(db)

@router.get("/{build_id}", response_model=build_schemas.Build)
def read_build_details(build_id: int, db: Session = Depends(db_session.get_db)):
    # Retrieve details for a specific build by its ID, including its stages.
    db_build = build_service.get_build_details(db, build_id=build_id)
    if db_build is None:
        raise HTTPException(status_code=404, detail="Build not found")
    return db_build
