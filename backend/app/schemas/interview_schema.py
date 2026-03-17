from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime


# ── Request schemas ────────────────────────────────────────────────────────────

class StartInterviewRequest(BaseModel):
    interview_type: str = Field(..., pattern="^(coding|system_design|behavioral)$")
    question_id: Optional[str] = None  # optional: pick a specific question

class MessageRequest(BaseModel):
    session_id: str
    user_message: str

class EvaluateRequest(BaseModel):
    session_id: str
    user_answer: Optional[str] = None  # optional extra answer text

class RunCodeRequest(BaseModel):
    language: str = Field(..., pattern="^(python|javascript|cpp)$")
    code: str
    test_cases: Optional[List[Dict[str, Any]]] = None
    session_id: Optional[str] = None

class SubmitCodeRequest(BaseModel):
    session_id: str
    language: str
    code: str


# ── Response schemas ───────────────────────────────────────────────────────────

class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StartInterviewResponse(BaseModel):
    session_id: str
    interview_type: str
    first_question: str
    question_id: Optional[str] = None
    question_title: Optional[str] = None
    question_difficulty: Optional[str] = None
    starter_code: Optional[Dict[str, str]] = None


class AIMessageResponse(BaseModel):
    session_id: str
    message: str
    role: str = "assistant"


class ScoreDimension(BaseModel):
    label: str
    score: int
    max_score: int = 10


class EvaluationResponse(BaseModel):
    session_id: str
    overall_score: float
    dimensions: List[ScoreDimension]
    strengths: List[str]
    areas_for_improvement: List[str]
    recommendations: List[str]
    summary: str


class TestResult(BaseModel):
    test_number: int
    passed: bool
    input: Any
    expected: Any
    actual: Any
    error: Optional[str] = None


class RunCodeResponse(BaseModel):
    passed_tests: int
    total_tests: int
    runtime_ms: Optional[float] = None
    memory_kb: Optional[float] = None
    results: List[TestResult]
    stdout: Optional[str] = None
    error: Optional[str] = None


class ReportResponse(BaseModel):
    session_id: str
    interview_type: str
    duration_seconds: int
    overall_score: Optional[float]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    messages: List[MessageResponse]
    created_at: Optional[datetime]
    completed_at: Optional[datetime]


class QuestionResponse(BaseModel):
    id: str
    title: str
    description: str
    difficulty: Optional[str]
    category: Optional[str]
    starter_code: Optional[Dict[str, str]]
    tags: Optional[List[str]]

    class Config:
        from_attributes = True
