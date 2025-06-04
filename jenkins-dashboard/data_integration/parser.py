from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, validator, Field

class TargetStageSchema(BaseModel):
    stage_node_id: Optional[str] = None
    stage_name: str
    stage_order: Optional[int] = None
    start_time: datetime
    duration_millis: int
    pause_duration_millis: int = 0
    status: str
    exec_node: Optional[str] = None
    stage_data: Optional[Dict[str, Any]] = None

class TargetBuildSchema(BaseModel):
    project: str
    mr_number: str
    build_number: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_millis: Optional[int] = None
    queue_duration_millis: int = 0
    status: str
    pipeline_url: Optional[str] = None
    commit_hash: Optional[str] = None
    branch_name: Optional[str] = None
    triggered_by: Optional[str] = None
    raw_data: Dict[str, Any]
    stages: List[TargetStageSchema] = []

    @validator('start_time', 'end_time', pre=True, allow_reuse=True)
    def ensure_datetime_obj(cls, v):
        if v is None: return None
        if isinstance(v, (int, float)): return datetime.fromtimestamp(v / 1000.0, tz=timezone.utc)
        if isinstance(v, str):
            try: return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError: raise ValueError(f"Invalid datetime string: {v}")
        if isinstance(v, datetime): return v
        raise TypeError(f"Unsupported type for datetime: {type(v)}")

def parse_jenkins_job_path_to_identifiers(job_path_segment: str) -> Dict[str, Optional[str]]:
    identifiers = {'project_display_name': None, 'mr_number': "N/A", 'branch_name': None}
    segments = [s for s in job_path_segment.split('/') if s != 'job']

    if not segments: return identifiers

    # Example logic: "job/group/job/repo/job/MR-123" or "job/project/job/branch"
    # This needs to be very flexible or configurable based on Jenkins structure.

    if len(segments) == 1: # e.g., "job/my-project"
        identifiers['project_display_name'] = segments[0]
        identifiers['branch_name'] = "main" # Default or assumption
    elif len(segments) >= 2: # e.g., "job/my-group/job/my-repo" or "job/my-project/job/my-branch"
        # Check if the last segment looks like an MR or is a common main/master branch
        last_segment = segments[-1]
        if last_segment.startswith("MR-") and last_segment.split('-')[-1].isdigit():
            identifiers['mr_number'] = last_segment.split('-')[-1]
            # Project name could be concatenation of prior segments
            identifiers['project_display_name'] = "-".join(segments[:-1])
        elif last_segment in ["main", "master", "develop", "production"]: # Common main branch names
            identifiers['branch_name'] = last_segment
            identifiers['project_display_name'] = "-".join(segments[:-1])
        else: # Assume last segment is a feature branch, and project is prior segments
            identifiers['branch_name'] = last_segment
            identifiers['project_display_name'] = "-".join(segments[:-1])
            # If project_display_name is empty, it means segments was like ["feature-branch"]
            if not identifiers['project_display_name'] and len(segments) ==1 :
                 identifiers['project_display_name'] = segments[0] # e.g. job/my-feature-branch -> project: my-feature-branch
                 identifiers['branch_name'] = segments[0]


    if not identifiers['project_display_name']: # Fallback
        identifiers['project_display_name'] = "UnknownProject"

    return identifiers

def parse_jenkins_build_data(raw_data: Dict[str, Any], jenkins_base_url: str, job_path_segment: str) -> Optional[TargetBuildSchema]:
    try:
        build_id_str = str(raw_data['id'])

        ids = parse_jenkins_job_path_to_identifiers(job_path_segment)
        project_name = ids['project_display_name']
        mr_number_val = ids['mr_number']
        branch_name_val = ids['branch_name']

        pipeline_url = f"{jenkins_base_url.rstrip('/')}/{job_path_segment.strip('/')}/{build_id_str}/"

        status_mapping = {
            "SUCCESS": "SUCCESS", "UNSTABLE": "UNSTABLE", "FAILURE": "FAILURE",
            "ABORTED": "ABORTED", "IN_PROGRESS": "IN_PROGRESS", "NOT_EXECUTED": "ABORTED"
        }
        build_status = status_mapping.get(raw_data.get('status', '').upper(), "FAILURE")

        parsed_stages = []
        if raw_data.get('stages'):
            for i, stage_raw in enumerate(raw_data['stages']):
                stage_status = status_mapping.get(stage_raw.get('status', '').upper(), "FAILURE")
                parsed_stages.append(
                    TargetStageSchema(
                        stage_node_id=stage_raw.get('id'),
                        stage_name=stage_raw.get('name', 'Unknown Stage'),
                        stage_order=i,
                        start_time=datetime.fromtimestamp(stage_raw['startTimeMillis'] / 1000.0, tz=timezone.utc),
                        duration_millis=stage_raw['durationMillis'],
                        pause_duration_millis=stage_raw.get('pauseDurationMillis', 0),
                        status=stage_status,
                        exec_node=stage_raw.get('execNode'),
                        stage_data=stage_raw
                    )
                )

        queue_duration = raw_data.get('queueDurationMillis', 0)
        if queue_duration is None: queue_duration = 0

        commit_hash_val = None
        display_name = raw_data.get('name', '')
        if display_name and " - " in display_name:
            possible_commit = display_name.split(" - ")[-1]
            if len(possible_commit) in [7, 8, 10, 12, 40]: # common git hash lengths
                 commit_hash_val = possible_commit

        # If it's an MR job, branch_name might be the source branch of MR, complex to get without more API calls.
        # If not MR job, branch_name_val from path parsing is used.

        build_data = TargetBuildSchema(
            project=project_name,
            mr_number=mr_number_val,
            build_number=build_id_str,
            start_time=raw_data['startTimeMillis'],
            end_time=raw_data.get('endTimeMillis'),
            duration_millis=raw_data.get('durationMillis'),
            queue_duration_millis=int(queue_duration),
            status=build_status,
            pipeline_url=pipeline_url,
            commit_hash=commit_hash_val,
            branch_name=branch_name_val if mr_number_val == "N/A" else None,
            triggered_by=None, # Placeholder, Jenkins API for this is complex
            raw_data=raw_data,
            stages=parsed_stages
        )
        return build_data
    except Exception as e:
        print(f"Error parsing Jenkins data (ID {raw_data.get('id')}, Job {job_path_segment}): {e}. Data: {str(raw_data)[:500]}")
        return None

if __name__ == '__main__':
    sample_wfapi_data = {
        "id": "52", "name": "#52 - feat/new-login-flow", "status": "SUCCESS",
        "startTimeMillis": 1700000000000, "endTimeMillis": 1700000500000, "durationMillis": 500000,
        "queueDurationMillis": 1200,
        "stages": [
            {"id": "s1", "name": "Checkout", "status": "SUCCESS", "startTimeMillis": 1700000001000, "durationMillis": 20000, "pauseDurationMillis": 0},
            {"id": "s2", "name": "Build", "status": "SUCCESS", "startTimeMillis": 1700000021000, "durationMillis": 300000, "pauseDurationMillis": 0},
            {"id": "s3", "name": "Test", "status": "SUCCESS", "startTimeMillis": 1700000321000, "durationMillis": 180000, "pauseDurationMillis": 0}
        ]
    }

    print("--- Test Case: Feature Branch Job ---")
    parsed_branch = parse_jenkins_build_data(sample_wfapi_data, "http://jenkins.example.com", "job/my-app/job/feat_new-login-flow")
    if parsed_branch: print(parsed_branch.json(indent=2))
    else: print("Failed.")

    print("\n--- Test Case: MR Job ---")
    sample_mr_data = {**sample_wfapi_data, "id": "10", "name": "#10"} # MR job might not have branch in name
    parsed_mr = parse_jenkins_build_data(sample_mr_data, "http://jenkins.example.com", "job/my-group/job/my-repo/job/MR-101")
    if parsed_mr: print(parsed_mr.json(indent=2))
    else: print("Failed.")

    print("\n--- Test Case: Main Branch Job ---")
    sample_main_data = {**sample_wfapi_data, "id": "200", "name": "#200"}
    parsed_main = parse_jenkins_build_data(sample_main_data, "http://jenkins.example.com", "job/another-app/job/main")
    if parsed_main: print(parsed_main.json(indent=2))
    else: print("Failed.")

    print("\n--- Test Case: Simple Project (no repo/branch in path) ---")
    parsed_simple = parse_jenkins_build_data(sample_wfapi_data, "http://jenkins.example.com", "job/utility-job")
    if parsed_simple: print(parsed_simple.json(indent=2))
    else: print("Failed.")
