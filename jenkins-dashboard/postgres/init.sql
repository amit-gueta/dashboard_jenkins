-- Main builds table
CREATE TABLE builds (
    id SERIAL PRIMARY KEY,
    project VARCHAR(150) NOT NULL, -- Increased length for "group-repo"
    mr_number VARCHAR(50) NOT NULL, -- "N/A" for non-MR builds or if not applicable
    build_number VARCHAR(50) NOT NULL,
    start_time TIMESTAMPTZ NULL, -- Can be null if build is created implicitly by a stage
    end_time TIMESTAMPTZ NULL,
    duration_millis BIGINT NULL,
    queue_duration_millis INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'IN_PROGRESS' NOT NULL CHECK (status IN ('SUCCESS', 'FAILURE', 'UNSTABLE', 'ABORTED', 'IN_PROGRESS', 'UNKNOWN')), -- Added UNKNOWN, default IN_PROGRESS
    pipeline_url TEXT NULL,
    commit_hash VARCHAR(40) NULL,
    branch_name VARCHAR(200) NULL,
    triggered_by VARCHAR(100) NULL,
    raw_data JSONB NULL, -- To store the first stage data or other context if needed
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(project, mr_number, build_number)
);

-- Stages table for detailed analysis
CREATE TABLE stages (
    id SERIAL PRIMARY KEY,
    build_id INTEGER REFERENCES builds(id) ON DELETE CASCADE NOT NULL, -- Ensure build_id is not null
    stage_node_id VARCHAR(50) NULL, -- Jenkins stage node ID from API
    stage_name VARCHAR(200) NOT NULL,
    stage_order INTEGER NULL, -- Order can be derived or explicitly set
    start_time TIMESTAMPTZ NULL, -- As per user feedback, can be null
    duration_millis BIGINT NULL, -- Duration can be null if not provided or applicable
    pause_duration_millis INTEGER DEFAULT 0,
    status VARCHAR(20) NOT NULL,
    exec_node VARCHAR(100) NULL,
    stage_data JSONB NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_builds_project_mr_build_num ON builds(project, mr_number, build_number); -- For unique constraint lookup
CREATE INDEX idx_builds_start_time ON builds(start_time DESC NULLS LAST); -- Allow nulls in sorted index
CREATE INDEX idx_stages_build_id_order ON stages(build_id, stage_order);
CREATE INDEX idx_stages_start_time ON stages(start_time DESC NULLS LAST);


-- Ensure stage status check constraint matches backend logic/parsing
-- Jenkins Blue Ocean statuses: SUCCESS, UNSTABLE, FAILURE, ABORTED, NOT_EXECUTED, IN_PROGRESS
-- Mapping 'NOT_EXECUTED' to 'SKIPPED' or 'ABORTED' is common.
-- The provided sample data uses "SUCCESS" and "UNSTABLE".
ALTER TABLE stages ADD CONSTRAINT check_stage_status CHECK (status IN ('SUCCESS', 'FAILURE', 'UNSTABLE', 'ABORTED', 'IN_PROGRESS', 'SKIPPED', 'NOT_EXECUTED', 'UNKNOWN'));

COMMENT ON COLUMN builds.project IS 'Composite project name, e.g., group-repo';
COMMENT ON COLUMN builds.status IS 'Overall status of the build, can be updated as stages progress';
COMMENT ON COLUMN stages.start_time IS 'Start time of the stage, can be null if not provided';
COMMENT ON COLUMN stages.duration_millis IS 'Duration of the stage, can be null';

EOF
