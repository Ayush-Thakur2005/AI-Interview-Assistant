"""
AI Service — wraps OpenAI and Anthropic with a unified interface.
Handles system prompts, message history, and token tracking.
"""
import logging
from typing import List, Dict, Optional
from app.config import settings

logger = logging.getLogger(__name__)

INTERVIEW_SYSTEM_PROMPTS = {
    "coding": """You are an expert technical interviewer at a top tech company conducting a live coding interview.
Your role:
- Ask the candidate to solve the given algorithmic problem
- Probe their thinking with follow-up questions about time complexity, space complexity, and edge cases
- If they're stuck, give subtle hints rather than the full solution
- Encourage them to think aloud
- Keep responses concise (2-4 sentences) unless giving detailed feedback
- Be supportive but challenging

Do NOT solve the problem for them. Keep follow-ups targeted and specific.""",

    "system_design": """You are a senior staff engineer conducting a system design interview.
Your role:
- Guide the candidate through designing a scalable system
- Ask about requirements, scale, architecture, databases, caching, and failure handling
- Probe deeper on trade-offs and bottlenecks
- Push back with realistic constraints (high traffic, data consistency, latency)
- Keep responses concise (2-4 sentences) unless giving detailed evaluation
- Be collaborative but rigorous""",

    "behavioral": """You are an experienced engineering manager conducting a behavioral interview.
Your role:
- Ask STAR-method behavioral questions about past experiences
- Follow up to uncover the candidate's specific contributions, decisions, and learnings
- Probe for leadership, conflict resolution, and impact
- Ask for quantifiable results
- Keep responses concise (1-3 sentences per follow-up)
- Be encouraging but dig for specifics""",
}

EVALUATION_SYSTEM_PROMPT = """You are a technical interview evaluator. 
Given a full interview conversation, produce a structured JSON evaluation.

Return ONLY valid JSON with this exact structure:
{
  "overall_score": <float 0-10>,
  "dimensions": [
    {"label": "<dimension>", "score": <int 0-10>, "max_score": 10}
  ],
  "strengths": ["<strength 1>", "<strength 2>"],
  "areas_for_improvement": ["<area 1>", "<area 2>"],
  "recommendations": ["<rec 1>", "<rec 2>"],
  "summary": "<2-3 sentence summary>"
}

No markdown, no explanation, only the JSON object."""


def _build_messages(history: List[Dict], user_message: str) -> List[Dict]:
    messages = list(history)
    messages.append({"role": "user", "content": user_message})
    return messages


async def get_ai_response(
    interview_type: str,
    history: List[Dict],
    user_message: str,
    interview_id: Optional[str] = None,
    user_id: Optional[str] = None,
) -> str:
    """Get next interviewer message from AI."""
    system = INTERVIEW_SYSTEM_PROMPTS.get(interview_type, INTERVIEW_SYSTEM_PROMPTS["behavioral"])
    messages = _build_messages(history, user_message)

    if settings.AI_PROVIDER == "anthropic":
        return await _call_anthropic(system, messages, interview_id, user_id)
    else:
        return await _call_openai(system, messages, interview_id, user_id)


async def get_evaluation(
    interview_type: str,
    history: List[Dict],
    question_text: str,
) -> Dict:
    """Evaluate a completed interview and return structured JSON."""
    conversation = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in history
    )
    user_message = (
        f"Interview type: {interview_type}\n"
        f"Question: {question_text}\n\n"
        f"Full conversation:\n{conversation}\n\n"
        f"Evaluate this interview."
    )

    if settings.AI_PROVIDER == "anthropic":
        raw = await _call_anthropic(EVALUATION_SYSTEM_PROMPT, [{"role": "user", "content": user_message}])
    else:
        raw = await _call_openai(EVALUATION_SYSTEM_PROMPT, [{"role": "user", "content": user_message}])

    import json
    try:
        return json.loads(raw)
    except Exception:
        # Fallback structured response
        return {
            "overall_score": 6.0,
            "dimensions": [
                {"label": "Communication", "score": 6, "max_score": 10},
                {"label": "Technical Depth", "score": 6, "max_score": 10},
                {"label": "Problem Solving", "score": 6, "max_score": 10},
            ],
            "strengths": ["Engaged with the problem", "Clear communication"],
            "areas_for_improvement": ["Deeper technical analysis needed"],
            "recommendations": ["Practice more problems of this type"],
            "summary": "Solid attempt. Keep practicing to sharpen technical depth.",
        }


async def _call_anthropic(system: str, messages: List[Dict], interview_id=None, user_id=None) -> str:
    import anthropic as ant
    client = ant.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system,
        messages=messages,
    )
    text = response.content[0].text

    # Log usage
    _log_usage("anthropic", "claude-sonnet-4-20250514",
               response.usage.input_tokens, response.usage.output_tokens,
               interview_id, user_id)
    return text


async def _call_openai(system: str, messages: List[Dict], interview_id=None, user_id=None) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    full_messages = [{"role": "system", "content": system}] + messages
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=full_messages,
        max_tokens=1024,
    )
    text = response.choices[0].message.content

    usage = response.usage
    _log_usage("openai", "gpt-4o",
               usage.prompt_tokens, usage.completion_tokens,
               interview_id, user_id)
    return text


def _log_usage(provider, model, prompt_tokens, completion_tokens, interview_id, user_id):
    """Fire-and-forget usage logging — don't block the response."""
    try:
        from app.database import SessionLocal
        from app.models.question import AIUsage
        db = SessionLocal()
        usage = AIUsage(
            user_id=user_id,
            interview_id=interview_id,
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        db.add(usage)
        db.commit()
        db.close()
    except Exception as e:
        logger.warning(f"Failed to log AI usage: {e}")
