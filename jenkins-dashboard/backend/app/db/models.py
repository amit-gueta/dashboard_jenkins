from sqlalchemy import Column, Integer, String, DateTime, BigInteger, JSON, ForeignKey, UniqueConstraint, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMPTZ, JSONB

Base = declarative_base()

class Build(Base):
    __tablename__ = "builds"

    id = Column(Integer, primary_key=True, index=True)
    project = Column(String(100), nullable=False)
    mr_number = Column(String(50), nullable=False)
    build_number = Column(Integer, nullable=False)
    start_time = Column(TIMESTAMPTZ, nullable=False)
    end_time = Column(TIMESTAMPTZ, nullable=True)
    duration_millis = Column(BigInteger, nullable=True)
    queue_duration_millis = Column(Integer, default=0)
    status = Column(String(20), nullable=False)  # Add CHECK constraint if possible or handle in app logic
    pipeline_url = Column(Text, nullable=True)
    commit_hash = Column(String(40), nullable=True)
    branch_name = Column(String(200), nullable=True)
    triggered_by = Column(String(100), nullable=True)
    raw_data = Column(JSONB, nullable=True) # Changed to JSONB from JSON
    created_at = Column(TIMESTAMPTZ, default=func.now())
    updated_at = Column(TIMESTAMPTZ, default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint('project', 'mr_number', 'build_number', name='uq_build_identifier'),)

class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(Integer, ForeignKey("builds.id", ondelete="CASCADE"))
    stage_node_id = Column(String(50), nullable=True)
    stage_name = Column(String(200), nullable=False)
    stage_order = Column(Integer, nullable=True)
    start_time = Column(TIMESTAMPTZ, nullable=False)
    duration_millis = Column(BigInteger, nullable=False)
    pause_duration_millis = Column(Integer, default=0)
    status = Column(String(20), nullable=False)
    exec_node = Column(String(100), nullable=True)
    stage_data = Column(JSONB, nullable=True) # Changed to JSONB from JSON
    created_at = Column(TIMESTAMPTZ, default=func.now())
