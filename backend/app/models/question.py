from sqlalchemy import Column, String, Text, DateTime, ARRAY, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True) 
    difficulty = Column(String(20), nullable=True)
    tags = Column(ARRAY(String), nullable=True)
    starter_code = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Note: AIUsage was dropped per new schema and InterviewQuestion handles mapping to sessions

class UserPerformance(Base):
    __tablename__ = "user_performance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    coding_score = Column(Float, nullable=True)
    system_design_score = Column(Float, nullable=True)
    behavioral_score = Column(Float, nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="performance")
