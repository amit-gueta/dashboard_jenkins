from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class StageBase(BaseModel):
    stage_node_id: Optional[str]
    stage_name: str
    stage_order: Optional[int]
    start_time: datetime
    duration_millis: int
    pause_duration_millis: Optional[int] = 0
    status: str
    exec_node: Optional[str]
    stage_data: Optional[dict]

class StageCreate(StageBase):
    pass

class Stage(StageBase):
    id: int
    build_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class BuildBase(BaseModel):
    project: str
    mr_number: str
    build_number: int
    start_time: datetime
    end_time: Optional[datetime]
    duration_millis: Optional[int]
    queue_duration_millis: Optional[int] = 0
    status: str
    pipeline_url: Optional[str]
    commit_hash: Optional[str]
    branch_name: Optional[str]
    triggered_by: Optional[str]
    raw_data: Optional[dict]

class BuildCreate(BuildBase):
    stages: Optional[List[StageCreate]] = []

class BuildUpdate(BuildBase):
    pass

class Build(BuildBase):
    id: int
    created_at: datetime
    updated_at: datetime
    stages: List[Stage] = []

    class Config:
        orm_mode = True

class BuildSyncRequest(BaseModel):
    project: Optional[str]
    full_sync: bool = False
