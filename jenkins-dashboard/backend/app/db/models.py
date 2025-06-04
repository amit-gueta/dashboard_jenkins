from sqlalchemy import Column, Integer, String, DateTime, BigInteger, JSON, ForeignKey, UniqueConstraint, Text, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMPTZ

Base = declarative_base()

class Build(Base):
    __tablename__ = "builds"
    id = Column(Integer, primary_key=True, index=True)
    project = Column(String(150), nullable=False)
    mr_number = Column(String(50), nullable=False, default="N/A")
    build_number = Column(String(50), nullable=False)
    start_time = Column(TIMESTAMPTZ, nullable=True)
    end_time = Column(TIMESTAMPTZ, nullable=True)
    duration_millis = Column(BigInteger, nullable=True)
    queue_duration_millis = Column(Integer, default=0, nullable=True)
    status = Column(String(20), nullable=False, default='IN_PROGRESS')
    pipeline_url = Column(Text, nullable=True)
    commit_hash = Column(String(40), nullable=True)
    branch_name = Column(String(200), nullable=True)
    triggered_by = Column(String(100), nullable=True)
    raw_data = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMPTZ, server_default=func.now())
    updated_at = Column(TIMESTAMPTZ, server_default=func.now(), onupdate=func.now())
    stages = relationship("Stage", back_populates="build", cascade="all, delete-orphan")
    __table_args__ = (
        UniqueConstraint('project', 'mr_number', 'build_number', name='uq_build_identifier'),
        CheckConstraint(status.in_(['SUCCESS', 'FAILURE', 'UNSTABLE', 'ABORTED', 'IN_PROGRESS', 'UNKNOWN']), name='ck_build_status')
    )

class Stage(Base):
    __tablename__ = "stages"
    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(Integer, ForeignKey("builds.id", ondelete="CASCADE"), nullable=False)
    stage_node_id = Column(String(50), nullable=True)
    stage_name = Column(String(200), nullable=False)
    stage_order = Column(Integer, nullable=True)
    start_time = Column(TIMESTAMPTZ, nullable=True)
    duration_millis = Column(BigInteger, nullable=True)
    pause_duration_millis = Column(Integer, default=0, nullable=True)
    status = Column(String(20), nullable=False)
    exec_node = Column(String(100), nullable=True)
    stage_data = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMPTZ, server_default=func.now())
    build = relationship("Build", back_populates="stages")
    __table_args__ = (
        CheckConstraint(status.in_(['SUCCESS', 'FAILURE', 'UNSTABLE', 'ABORTED', 'IN_PROGRESS', 'SKIPPED', 'NOT_EXECUTED', 'UNKNOWN']), name='ck_stage_status'),
    )
