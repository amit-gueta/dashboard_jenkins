from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import session as db_session
from app.schemas.build import StageIngress, BuildCreate, StageCreate, Stage as StageResponseSchema
from app.services import build_service
from typing import Optional
from datetime import datetime

router = APIRouter()

@router.post("/stage", status_code=201, response_model=StageResponseSchema)
def ingress_stage_data(
    *,
    db: Session = Depends(db_session.get_db),
    stage_payload: StageIngress
):
    # Simplified: Ingests stage data.
    project_identifier = f"{stage_payload.group}-{stage_payload.repo}"

    db_build = build_service.get_build_by_identifiers(
        db,
        project=project_identifier,
        mr_number=stage_payload.MR_num,
        build_number=stage_payload.build_num
    )

    parsed_start_time: Optional[datetime] = stage_payload.startTime

    if not db_build:
        url_parts = stage_payload.pipeURL.strip('/').split('/')
        base_pipeline_url = "/".join(url_parts[:-1]) + "/" if len(url_parts) > 1 else stage_payload.pipeURL

        build_create_data = BuildCreate(
            project=project_identifier,
            mr_number=stage_payload.MR_num,
            build_number=stage_payload.build_num,
            pipeline_url=base_pipeline_url,
            status='IN_PROGRESS',
            start_time=parsed_start_time,
            raw_data={"source_pipeURL": stage_payload.pipeURL, "group": stage_payload.group, "repo": stage_payload.repo}
        )
        db_build = build_service.create_build(db, build_data=build_create_data)

    stage_create_data = StageCreate(
        build_id=db_build.id,
        stage_name=stage_payload.displayName,
        start_time=parsed_start_time,
        duration_millis=stage_payload.durationInMillis,
        status=stage_payload.result.upper(),
        stage_data=stage_payload.dict()
    )

    db_stage = build_service.create_stage_for_build(db, stage_data=stage_create_data)
    return db_stage
