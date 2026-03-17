"""
Evaluation Service — handles scoring, feedback generation, and report assembly.
"""
import logging
from datetime import datetime, timezone
from typing import Dict, List
from sqlalchemy.orm import Session

from app.models.interview import InterviewSession, InterviewMessage

logger = logging.getLogger(__name__)

DIMENSION_MAP = {
    "coding": [
        "Correctness",
        "Time Complexity",
        "Space Complexity",
        "Code Clarity",
        "Edge Case Handling",
    ],
    "system_design": [
        "Architecture Clarity",
        "Scalability",
        "Database Design",
        "Caching Strategy",
        "Trade-off Analysis",
    ],
    "behavioral": [
        "Communication Clarity",
        "STAR Structure",
        "Leadership Evidence",
        "Problem Solving",
        "Self-Awareness",
    ],
}


async def evaluate_interview(db: Session, session_id: str, extra_answer: str = "") -> Dict:
    interview = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not interview:
        raise ValueError(f"Session {session_id} not found.")

    # Append extra answer if provided
    if extra_answer:
        db.add(InterviewMessage(session_id=session_id, role="user", message=extra_answer))
        db.commit()

    history = [
        {"role": m.role, "content": m.message}
        for m in db.query(InterviewMessage)
        .filter(InterviewMessage.session_id == session_id)
        .order_by(InterviewMessage.created_at)

        .all()
    ]

    question_text = interview.question_text or ""
    evaluation = await get_evaluation(
        interview_type=interview.interview_type,
        history=history,
        question_text=question_text,
    )

    # Ensure dimensions match interview type
    if not evaluation.get("dimensions"):
        dims = DIMENSION_MAP.get(interview.interview_type, [])
        evaluation["dimensions"] = [
            {"label": d, "score": int(evaluation.get("overall_score", 6)), "max_score": 10}
            for d in dims
        ]

    # Persist evaluation & mark complete
    interview.overall_score = evaluation.get("overall_score")
    interview.feedback = evaluation
    interview.status = "completed"
    interview.completed_at = datetime.now(timezone.utc)
    db.commit()

    return {
        "session_id": session_id,
        "overall_score": evaluation.get("overall_score", 0),
        "dimensions": evaluation.get("dimensions", []),
        "strengths": evaluation.get("strengths", []),
        "areas_for_improvement": evaluation.get("areas_for_improvement", []),
        "recommendations": evaluation.get("recommendations", []),
        "summary": evaluation.get("summary", ""),
    }


def build_report(db: Session, session_id: str) -> Dict:
    interview = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not interview:
        raise ValueError(f"Session {session_id} not found.")

    messages = (
        db.query(InterviewMessage)
        .filter(InterviewMessage.session_id == session_id)
        .order_by(InterviewMessage.created_at)
        .all()
    )

    feedback = interview.feedback or {}
    duration = 0
    if interview.completed_at and interview.created_at:
        delta = interview.completed_at - interview.created_at
        duration = int(delta.total_seconds())

    return {
        "session_id": session_id,
        "interview_type": interview.interview_type,
        "duration_seconds": duration,
        "overall_score": interview.overall_score,
        "strengths": feedback.get("strengths", []),
        "weaknesses": feedback.get("areas_for_improvement", []),
        "recommendations": feedback.get("recommendations", []),
        "messages": [
            {"role": m.role, "content": m.message, "created_at": m.created_at}
            for m in messages
        ],
        "created_at": interview.created_at,
        "completed_at": interview.completed_at,
    }
