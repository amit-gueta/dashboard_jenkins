// Based on backend Pydantic schemas

export interface Stage {
  id: number;
  build_id: number;
  stage_name: string;
  stage_node_id?: string | null;
  stage_order?: number | null;
  start_time?: string | null; // ISO datetime string
  duration_millis?: number | null;
  pause_duration_millis?: number;
  status: string; // SUCCESS, FAILURE, etc.
  exec_node?: string | null;
  stage_data?: Record<string, any> | null;
  created_at: string; // ISO datetime string
}

export interface Build {
  id: number;
  project: string; // "group-repo"
  mr_number: string;
  build_number: string;
  start_time?: string | null; // ISO datetime string
  end_time?: string | null; // ISO datetime string
  duration_millis?: number | null;
  queue_duration_millis?: number;
  status: string; // SUCCESS, FAILURE, etc.
  pipeline_url?: string | null;
  commit_hash?: string | null;
  branch_name?: string | null;
  triggered_by?: string | null;
  raw_data?: Record<string, any> | null;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
  stages: Stage[];
}
