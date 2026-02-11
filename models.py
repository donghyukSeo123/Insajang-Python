from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# 1. 프로젝트 모델 (최소 정보만 정의)
class Project(Base):
    __tablename__ = "projects"

    project_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    # 관계 설정 (선택 사항이지만 있으면 편리함)
    contents = relationship("Content", back_populates="project")

# 2. 컨텐츠 모델 (보내주신 SQL 완벽 반영)
class Content(Base):
    __tablename__ = "contents"

    content_id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String(255))
    body = Column(Text, nullable=False)
    content_type = Column(String(50))
    status = Column(String(50), default="DRAFT")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scheduled_at = Column(DateTime)
    
    type = Column(String(255), nullable=False)

    # 관계 설정
    project = relationship("Project", back_populates="contents")