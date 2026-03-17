"""
Interview routes — session management, messaging, evaluation, reports.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.schemas.interview_schema import (
    StartInterviewRequest, StartInterviewResponse,
    MessageRequest, AIMessageResponse,
    EvaluateRequest, EvaluationResponse,
    ReportResponse, SubmitCodeRequest,
)
from app.services import interview_service, evaluation_service
from app.models.user import User

router = APIRouter(prefix="/interview", tags=["interview"])
logger = logging.getLogger(__name__)


def _ensure_user(db: Session, current_user: dict):
    """Upsert the Supabase user into local DB."""
    interview_service.get_or_create_user(
        db,
        user_id=current_user["user_id"],
        email=current_user["email"],
        full_name=current_user.get("full_name"),
    )


@router.post("/start", response_model=StartInterviewResponse)
async def start_interview(
    body: StartInterviewRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new interview session and return the opening question."""
    _ensure_user(db, current_user)
    try:
        result = interview_service.start_interview(
            db=db,
            user_id=current_user["user_id"],
            interview_type=body.interview_type,
            question_id=body.question_id,
        )
        return result
    except Exception as e:
        logger.exception("Failed to start interview")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message", response_model=AIMessageResponse)
async def send_message(
    body: MessageRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Send a user message and receive the AI interviewer's response."""
    try:
        reply = await interview_service.process_message(
            db=db,
            session_id=body.session_id,
            user_message=body.user_message,
            user_id=current_user["user_id"],
        )
        return {"session_id": body.session_id, "message": reply, "role": "assistant"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Failed to process message")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_interview(
    body: EvaluateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Evaluate the full interview and return structured scores and feedback."""
    try:
        result = await evaluation_service.evaluate_interview(
            db=db,
            session_id=body.session_id,
            extra_answer=body.user_answer or "",
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Failed to evaluate interview")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit-code")
async def submit_code(
    body: SubmitCodeRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Submit code for AI review — triggers evaluation with code context."""
    try:
        code_context = f"[Code submitted in {body.language}]\n```{body.language}\n{body.code}\n```"
        reply = await interview_service.process_message(
            db=db,
            session_id=body.session_id,
            user_message=code_context,
            user_id=current_user["user_id"],
        )
        return {"session_id": body.session_id, "message": reply, "role": "assistant"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Failed to submit code")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/{session_id}", response_model=ReportResponse)
async def get_report(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Retrieve full report for a completed interview session."""
    try:
        report = evaluation_service.build_report(db, session_id)
        return report
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Failed to build report")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions")
async def list_sessions(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """List all interview sessions for the current user."""
    from app.mcp_tools.analytics_tool import get_user_history
    history = get_user_history(db, current_user["user_id"])
    return {"sessions": history}
