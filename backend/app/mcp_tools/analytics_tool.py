"""
MCP Tool: Analytics
Computes user performance metrics across sessions.
"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.interview import InterviewSession, InterviewMessage


ANALYTICS_TOOL_DESCRIPTOR = {
    "name": "get_user_analytics",
    "description": "Retrieve performance metrics and history for a user to personalise the interview.",
    "input_schema": {
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "interview_type": {"type": "string", "enum": ["coding", "system_design", "behavioral"]},
        },
        "required": ["user_id"],
    },
}


def get_user_analytics(db: Session, user_id: str, interview_type: Optional[str] = None) -> Dict:
    query = db.query(InterviewSession).filter(
        InterviewSession.user_id == user_id,
        InterviewSession.status == "completed",
    )
    if interview_type:
        query = query.filter(InterviewSession.interview_type == interview_type)

    completed = query.all()
    if not completed:
        return {
            "total_interviews": 0,
            "avg_score": None,
            "by_type": {},
            "recent_scores": [],
            "improvement_trend": "insufficient_data",
        }

    scores = [i.overall_score for i in completed if i.overall_score is not None]
    avg = round(sum(scores) / len(scores), 2) if scores else None

    by_type: Dict[str, List] = {}
    for i in completed:
        by_type.setdefault(i.interview_type, [])
        if i.overall_score:
            by_type[i.interview_type].append(i.overall_score)

    type_averages = {k: round(sum(v) / len(v), 2) for k, v in by_type.items() if v}

    recent = sorted(completed, key=lambda x: x.created_at, reverse=True)[:5]
    recent_scores = [
        {"interview_id": i.id, "type": i.interview_type, "score": i.overall_score, "date": str(i.created_at)}
        for i in recent
    ]

    trend = "improving"
    if len(scores) >= 3:
        if scores[-1] < scores[0]:
            trend = "declining"
        elif abs(scores[-1] - scores[0]) < 0.5:
            trend = "stable"

    return {
        "total_interviews": len(completed),
        "avg_score": avg,
        "by_type": type_averages,
        "recent_scores": recent_scores,
        "improvement_trend": trend,
    }


def get_user_history(db: Session, user_id: str, limit: int = 10) -> List[Dict]:
    interviews = (
        db.query(InterviewSession)
        .filter(InterviewSession.user_id == user_id)
        .order_by(InterviewSession.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "session_id": i.id,
            "type": i.interview_type,
            "status": i.status,
            "score": i.overall_score,
            "created_at": str(i.created_at),
        }
        for i in interviews
    ]
