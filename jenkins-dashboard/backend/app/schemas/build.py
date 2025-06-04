from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class StageIngress(BaseModel):
    pipeURL: str
    group: str
    repo: str
    MR_num: str = Field(alias="MR_num")
    build_num: str
    displayName: str
    durationInMillis: Optional[int] = None
    result: str
    startTime: Optional[str] = None # String from input, validated to datetime

    @validator('startTime', pre=True, allow_reuse=True)
    def format_starttime(cls, v: Optional[str]) -> Optional[datetime]:
        if v is None: return None
        if isinstance(v, str):
            try:
                # Handle timezone +0300 -> +03:00 by adjusting the string
                if '+' in v and ':' not in v[v.rfind('+'):len(v)]:
                    plus_index = v.rfind('+')
                    if len(v[plus_index:]) == 5: # Format +HHMM
                         v = v[:plus_index+3] + ":" + v[plus_index+3:]
                return datetime.fromisoformat(v)
            except ValueError as e:
                raise ValueError(f"Invalid startTime string format: '{v}'. Error: {e}")
        elif isinstance(v, datetime): return v
        raise TypeError(f"startTime must be a string or datetime, received {type(v)}")

# --- Other schemas needed by ingress.py and its dependencies ---
class StageBase(BaseModel):
    stage_name: str
    stage_node_id: Optional[str] = None
    stage_order: Optional[int] = None
    start_time: Optional[datetime] = None
    duration_millis: Optional[int] = None
    pause_duration_millis: Optional[int] = Field(default=0)
    status: str
    exec_node: Optional[str] = None
    stage_data: Optional[Dict[str, Any]] = None

class StageCreate(StageBase):
    build_id: int

class Stage(StageBase): # Response schema for a stage
    id: int
    build_id: int
    created_at: datetime
    class Config: orm_mode = True

class BuildBase(BaseModel):
    project: str
    mr_number: str = Field(default="N/A")
    build_number: str
    start_time: Optional[datetime] = None
    # Add other fields as they were defined before, ensuring BuildCreate can be used by ingress.py
    end_time: Optional[datetime] = None
    duration_millis: Optional[int] = None
    queue_duration_millis: Optional[int] = Field(default=0)
    status: str = Field(default='IN_PROGRESS')
    pipeline_url: Optional[str] = None
    commit_hash: Optional[str] = None
    branch_name: Optional[str] = None
    triggered_by: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None


class BuildCreate(BuildBase): pass

class Build(BuildBase): # For response if needed, not directly by ingress.py's stage response
    id: int
    created_at: datetime
    updated_at: datetime
    stages: List[Stage] = []
    class Config: orm_mode = True

EOF
