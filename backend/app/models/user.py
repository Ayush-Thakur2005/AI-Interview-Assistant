from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String(255), nullable=True)
    experience_level = Column(String(50), nullable=True)
    target_role = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    interviews = relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")
    performance = relationship("UserPerformance", back_populates="user", cascade="all, delete-orphan", uselist=False)
