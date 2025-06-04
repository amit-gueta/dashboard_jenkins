from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.db import models
from app.schemas import build as build_schemas
from datetime import datetime

def get_build_by_identifiers(db: Session, project: str, mr_number: str, build_number: str) -> Optional[models.Build]:
    return db.query(models.Build).filter(
        models.Build.project == project,
        models.Build.mr_number == mr_number,
        models.Build.build_number == build_number
    ).first()

def create_build(db: Session, build_data: build_schemas.BuildCreate) -> models.Build:
    # Use exclude_unset=True to respect default values in model if not provided in BuildCreate
    db_build = models.Build(**build_data.dict(exclude_unset=True))
    db.add(db_build)
    db.commit()
    db.refresh(db_build)
    return db_build

def create_stage_for_build(db: Session, stage_data: build_schemas.StageCreate) -> models.Stage:
    db_stage = models.Stage(**stage_data.dict())
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage

def get_builds_by_project(db: Session, project: str, skip: int = 0, limit: int = 100) -> List[models.Build]:
    # Eagerly load stages
    return db.query(models.Build).options(joinedload(models.Build.stages)).filter(models.Build.project == project).order_by(models.Build.start_time.desc().nullslast(), models.Build.id.desc()).offset(skip).limit(limit).all()

def get_all_builds(db: Session, skip: int = 0, limit: int = 100) -> List[models.Build]:
     # Eagerly load stages
     return db.query(models.Build).options(joinedload(models.Build.stages)).order_by(models.Build.start_time.desc().nullslast(), models.Build.id.desc()).offset(skip).limit(limit).all()

def get_build_details(db: Session, build_id: int) -> Optional[models.Build]:
    # Eagerly load stages
    return db.query(models.Build).options(joinedload(models.Build.stages)).filter(models.Build.id == build_id).first()

def get_distinct_projects(db: Session) -> List[str]:
    results = db.query(models.Build.project).distinct().order_by(models.Build.project).all()
    return [result[0] for result in results]
