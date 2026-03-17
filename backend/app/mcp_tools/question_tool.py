"""
MCP Tool: Question Retrieval
Fetches questions from the database for the AI to use during interviews.
"""
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from app.models.question import Question


def fetch_questions(
    db: Session,
    interview_type: str,
    difficulty: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 5,
) -> List[Dict]:
    """Retrieve questions matching criteria."""
    query = db.query(Question).filter(Question.interview_type == interview_type)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    if category:
        query = query.filter(Question.category == category)
    questions = query.limit(limit).all()
    return [
        {
            "id": q.id,
            "title": q.title,
            "description": q.description,
            "difficulty": q.difficulty,
            "category": q.category,
            "starter_code": q.starter_code,
            "test_cases": q.test_cases,
        }
        for q in questions
    ]


def fetch_question_by_id(db: Session, question_id: str) -> Optional[Dict]:
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        return None
    return {
        "id": q.id,
        "title": q.title,
        "description": q.description,
        "difficulty": q.difficulty,
        "starter_code": q.starter_code,
        "test_cases": q.test_cases,
    }


# MCP tool descriptor (for integration with MCP server)
QUESTION_TOOL_DESCRIPTOR = {
    "name": "fetch_questions",
    "description": "Retrieve interview questions from the database by type and difficulty.",
    "input_schema": {
        "type": "object",
        "properties": {
            "interview_type": {
                "type": "string",
                "enum": ["coding", "system_design", "behavioral"],
                "description": "The type of interview question to retrieve.",
            },
            "difficulty": {
                "type": "string",
                "enum": ["Easy", "Medium", "Hard"],
                "description": "Optional difficulty filter.",
            },
            "limit": {
                "type": "integer",
                "default": 5,
                "description": "Max number of questions to return.",
            },
        },
        "required": ["interview_type"],
    },
}
