-- Main builds table
CREATE TABLE builds (
    id SERIAL PRIMARY KEY,
    project VARCHAR(100) NOT NULL,
    mr_number VARCHAR(50) NOT NULL, -- "N/A" for non-MR builds
    build_number VARCHAR(50) NOT NULL, -- Jenkins build IDs can be non-integer strings from some APIs
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ,
    duration_millis BIGINT,
    queue_duration_millis INTEGER DEFAULT 0,
    status VARCHAR(20) NOT NULL CHECK (status IN ('SUCCESS', 'FAILURE', 'UNSTABLE', 'ABORTED', 'IN_PROGRESS')),
    pipeline_url TEXT,
    commit_hash VARCHAR(40),
    branch_name VARCHAR(200),
    triggered_by VARCHAR(100),
    raw_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(project, mr_number, build_number)
);

-- Stages table for detailed analysis
CREATE TABLE stages (
    id SERIAL PRIMARY KEY,
    build_id INTEGER REFERENCES builds(id) ON DELETE CASCADE,
    stage_node_id VARCHAR(50), -- Jenkins stage node ID from API
    stage_name VARCHAR(200) NOT NULL,
    stage_order INTEGER,
    start_time TIMESTAMPTZ NOT NULL,
    duration_millis BIGINT NOT NULL,
    pause_duration_millis INTEGER DEFAULT 0,
    status VARCHAR(20) NOT NULL, -- Should align with build statuses
    exec_node VARCHAR(100),
    stage_data JSONB, -- Store raw stage JSON from Jenkins if needed
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Optional: Indexes for performance
CREATE INDEX idx_builds_project_start_time ON builds(project, start_time DESC);
CREATE INDEX idx_builds_status ON builds(status);
CREATE INDEX idx_builds_branch_name ON builds(branch_name);
CREATE INDEX idx_stages_build_id ON stages(build_id);
CREATE INDEX idx_stages_stage_name ON stages(stage_name);

-- You might want a table for projects if you need to store metadata about them
-- CREATE TABLE projects (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(100) UNIQUE NOT NULL,
--     description TEXT,
--     created_at TIMESTAMPTZ DEFAULT NOW()
-- );

-- Note: CHECK constraint for status in 'stages' table might be needed too,
-- similar to 'builds' table, if its status values are strictly controlled.
-- Consider adding it if necessary.
ALTER TABLE stages ADD CONSTRAINT check_stage_status CHECK (status IN ('SUCCESS', 'FAILURE', 'UNSTABLE', 'ABORTED', 'IN_PROGRESS', 'SKIPPED', 'NOT_EXECUTED'));
-- Expanded stage statuses slightly, align with parser mapping.
