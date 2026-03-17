from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    interview_type = Column(String(50), nullable=True)
    status = Column(String(50), default="active")
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="interviews")
    messages = relationship("InterviewMessage", back_populates="interview_session", cascade="all, delete-orphan", order_by="InterviewMessage.created_at")
    code_submissions = relationship("CodeSubmission", back_populates="interview_session", cascade="all, delete-orphan")
    questions_mapping = relationship("InterviewQuestion", back_populates="interview_session", cascade="all, delete-orphan", order_by="InterviewQuestion.order_index")
    evaluations = relationship("Evaluation", back_populates="interview_session", cascade="all, delete-orphan")
    report = relationship("InterviewReport", back_populates="interview_session", cascade="all, delete-orphan", uselist=False)

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    order_index = Column(Integer, nullable=True)

    interview_session = relationship("InterviewSession", back_populates="questions_mapping")
    question = relationship("Question")

class CodeSubmission(Base):
    __tablename__ = "code_submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=True)
    language = Column(String(50), nullable=True)
    code = Column(Text, nullable=True)
    runtime = Column(Float, nullable=True)
    memory_usage = Column(Float, nullable=True)
    passed_tests = Column(Integer, nullable=True)
    total_tests = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interview_session = relationship("InterviewSession", back_populates="code_submissions")

class InterviewMessage(Base):
    __tablename__ = "interview_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=True) # user or ai
    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interview_session = relationship("InterviewSession", back_populates="messages")

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=True)
    correctness_score = Column(Float, nullable=True)
    clarity_score = Column(Float, nullable=True)
    optimization_score = Column(Float, nullable=True)
    communication_score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interview_session = relationship("InterviewSession", back_populates="evaluations")

class InterviewReport(Base):
    __tablename__ = "interview_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False)
    overall_score = Column(Float, nullable=True)
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interview_session = relationship("InterviewSession", back_populates="report")
