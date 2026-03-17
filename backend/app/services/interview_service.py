"""
Interview Service — session lifecycle, message persistence, and history.
"""
import logging
from datetime import datetime, timezone
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from app.models.interview import InterviewSession, InterviewMessage, InterviewQuestion
from app.models.user import User
from app.services.ai_service import get_ai_response, INTERVIEW_SYSTEM_PROMPTS

logger = logging.getLogger(__name__)


# ── Question selection ─────────────────────────────────────────────────────────

FALLBACK_QUESTIONS = {
    "coding": {
        "id": "two-sum",
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": (
            "Given an array of integers `nums` and an integer `target`, return indices of the two numbers "
            "that add up to target.\n\nExample:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]"
        ),
        "starter_code": {
            "python": "def two_sum(nums, target):\n    # Your code here\n    pass",
            "javascript": "function twoSum(nums, target) {\n  // Your code here\n}",
            "cpp": "#include <vector>\nusing namespace std;\n\nvector<int> twoSum(vector<int>& nums, int target) {\n    // Your code here\n}",
        },
    },
    "system_design": {
        "id": "url-shortener",
        "title": "Design a URL Shortener",
        "difficulty": "Medium",
        "description": "Design a scalable URL shortener service like bit.ly that can handle millions of requests per day.",
        "starter_code": None,
    },
    "behavioral": {
        "id": "conflict-resolution",
        "title": "Conflict Resolution",
        "difficulty": None,
        "description": "Tell me about a time you had to resolve a conflict within your team.",
        "starter_code": None,
    },
}


def _get_opening_message(interview_type: str, question: Dict) -> str:
    if interview_type == "coding":
        return (
            f"Welcome to your coding interview! Let's work on: **{question['title']}** ({question.get('difficulty','')}).\n\n"
            f"{question['description']}\n\n"
            "Take a moment to read the problem. When you're ready, walk me through your initial thinking — "
            "what approach comes to mind first?"
        )
    elif interview_type == "system_design":
        return (
            f"Welcome to your system design interview.\n\n**{question['description']}**\n\n"
            "Before jumping into the design, let's clarify requirements:\n"
            "1. What are the core features you'd prioritize?\n"
            "2. What scale are we designing for? (DAU, requests/sec)\n"
            "3. Any specific constraints or assumptions?\n\n"
            "Go ahead and set the scope."
        )
    else:  # behavioral
        return (
            f"Let's begin the behavioral interview.\n\n**{question['description']}**\n\n"
            "Take a moment to think, then use the STAR method:\n"
            "- **Situation:** Set the context\n"
            "- **Task:** Your responsibility\n"
            "- **Action:** What you did\n"
            "- **Result:** The outcome\n\n"
            "Go ahead whenever you're ready."
        )


def get_or_create_user(db: Session, user_id: str, email: str, full_name: Optional[str] = None) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, email=email, full_name=full_name)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def start_interview(
    db: Session,
    user_id: str,
    interview_type: str,
    question_id: Optional[str] = None,
) -> Dict:
    # Try DB question first, then fallback
    question_obj = None
    if question_id:
        question_obj = db.query(InterviewQuestion).filter(InterviewQuestion.question_id == question_id).first()
    if not question_obj:
        question_obj = (
            db.query(InterviewQuestion)
            .filter(Question.interview_type == interview_type)
            .order_by(Question.id)
            .first()
        )

    if question_obj and hasattr(question_obj, "question"):
        q_obj = question_obj.question
        question = {
            "id": q_obj.id,
            "title": q_obj.title,
            "difficulty": q_obj.difficulty,
            "description": q_obj.description,
            "starter_code": q_obj.starter_code,
        }
    else:
        question = FALLBACK_QUESTIONS.get(interview_type, FALLBACK_QUESTIONS["behavioral"])

    opening = _get_opening_message(interview_type, question)

    interview = InterviewSession(
        user_id=user_id,
        interview_type=interview_type,
        status="active",
    )
    db.add(interview)
    db.flush()

    # Persist opening assistant message
    msg = InterviewMessage(session_id=interview.id, role="assistant", message=opening)
    db.add(msg)
    db.commit()
    db.refresh(interview)

    return {
        "session_id": interview.id,
        "interview_type": interview_type,
        "first_question": opening,
        "question_id": question.get("id"),
        "question_title": question.get("title"),
        "question_difficulty": question.get("difficulty"),
        "starter_code": question.get("starter_code"),
    }


def get_history(db: Session, session_id: str) -> List[Dict]:
    messages = (
        db.query(InterviewMessage)
        .filter(InterviewMessage.session_id == session_id)
        .order_by(InterviewMessage.created_at)
        .all()
    )
    return [{"role": m.role, "content": m.message} for m in messages]


async def process_message(
    db: Session,
    session_id: str,
    user_message: str,
    user_id: str,
) -> str:
    interview = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not interview or interview.status != "active":
        raise ValueError("Session not found or already completed.")

    history = get_history(db, session_id)
    ai_reply = await get_ai_response(
        interview_type=interview.interview_type,
        history=history,
        user_message=user_message,
        interview_id=session_id,
        user_id=user_id,
    )

    # Persist both messages
    db.add(InterviewMessage(session_id=session_id, role="user", message=user_message))
    db.add(InterviewMessage(session_id=session_id, role="assistant", message=ai_reply))
    db.commit()

    return ai_reply


def get_interview(db: Session, session_id: str) -> Optional[InterviewSession]:
    return db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
