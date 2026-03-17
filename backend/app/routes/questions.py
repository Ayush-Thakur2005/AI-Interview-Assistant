"""
Question routes — CRUD and retrieval for interview questions.
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models.question import Question
from app.schemas.interview_schema import QuestionResponse
from app.mcp_tools.question_tool import fetch_questions

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=List[QuestionResponse])
async def list_questions(
    interview_type: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """List questions, optionally filtered by type and difficulty."""
    if interview_type:
        questions = fetch_questions(db, interview_type, difficulty=difficulty, limit=limit)
        return questions
    else:
        qs = db.query(Question).limit(limit).all()
        return qs


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found.")
    return q


@router.post("/", response_model=QuestionResponse, status_code=201)
async def create_question(
    body: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Admin: seed a new question."""
    q = Question(**body)
    db.add(q)
    db.commit()
    db.refresh(q)
    return q
