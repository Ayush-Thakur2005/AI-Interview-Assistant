"""
AI routes — direct AI interactions, code execution, analytics.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.schemas.interview_schema import RunCodeRequest, RunCodeResponse
from app.mcp_tools.code_runner import run_code
from app.mcp_tools.analytics_tool import get_user_analytics, get_user_history

router = APIRouter(prefix="/ai", tags=["ai"])
logger = logging.getLogger(__name__)


@router.post("/code/run", response_model=RunCodeResponse)
async def run_code_endpoint(
    body: RunCodeRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Execute code in a sandbox against provided test cases.
    Returns pass/fail results and runtime stats.
    """
    try:
        result = run_code(
            language=body.language,
            code=body.code,
            test_cases=body.test_cases or [],
        )
        return result
    except Exception as e:
        logger.exception("Code execution failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics")
async def get_analytics(
    interview_type: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Return performance analytics for the current user."""
    return get_user_analytics(db, current_user["user_id"], interview_type)


@router.get("/history")
async def get_history(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Return recent interview sessions for the current user."""
    return {"history": get_user_history(db, current_user["user_id"], limit=limit)}
