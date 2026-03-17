# InterviewOS — FastAPI Backend

AI-powered technical interview simulator backend built with FastAPI, PostgreSQL (Neon), Supabase Auth, and Anthropic/OpenAI.

---

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Pydantic settings from .env
│   ├── database.py          # SQLAlchemy engine + session
│   ├── auth.py              # Supabase JWT verification
│   ├── models/
│   │   ├── user.py          # User table
│   │   ├── interview.py     # Interview, Message, Submission tables
│   │   └── question.py      # Question + AIUsage tables
│   ├── schemas/
│   │   └── interview_schema.py   # Pydantic request/response models
│   ├── routes/
│   │   ├── interview.py     # /interview/* endpoints
│   │   ├── questions.py     # /questions/* endpoints
│   │   └── ai.py            # /ai/* endpoints (code run, analytics)
│   ├── services/
│   │   ├── ai_service.py         # Anthropic/OpenAI wrapper
│   │   ├── interview_service.py  # Session lifecycle
│   │   └── evaluation_service.py # Scoring & reports
│   └── mcp_tools/
│       ├── question_tool.py   # MCP: fetch questions
│       ├── code_runner.py     # MCP: sandbox code execution
│       └── analytics_tool.py  # MCP: user performance metrics
├── seed_questions.py        # DB seed script
├── requirements.txt
├── Dockerfile
└── .env.example
```

---

## Quick Start

### 1. Clone and install

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

Required variables:
| Variable | Description |
|---|---|
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `SUPABASE_JWT_SECRET` | Found in Supabase → Settings → API → JWT Secret |
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `OPENAI_API_KEY` | Your OpenAI API key (if using OpenAI) |
| `AI_PROVIDER` | `anthropic` or `openai` |
| `CORS_ORIGINS` | Comma-separated frontend URLs |

### 3. Initialize database & seed

```bash
python seed_questions.py
```

### 4. Run development server

```bash
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

---

## API Reference

### Interview Sessions

| Method | Endpoint | Description |
|---|---|---|
| POST | `/interview/start` | Start a new interview session |
| POST | `/interview/message` | Send message, get AI response |
| POST | `/interview/evaluate` | Evaluate and score interview |
| POST | `/interview/submit-code` | Submit code for AI review |
| GET | `/interview/report/{session_id}` | Get full interview report |
| GET | `/interview/sessions` | List user's past sessions |

### Questions

| Method | Endpoint | Description |
|---|---|---|
| GET | `/questions/` | List questions (filter by type/difficulty) |
| GET | `/questions/{id}` | Get single question |
| POST | `/questions/` | Create question (admin) |

### AI & Code

| Method | Endpoint | Description |
|---|---|---|
| POST | `/ai/code/run` | Execute code against test cases |
| GET | `/ai/analytics` | User performance analytics |
| GET | `/ai/history` | Recent interview history |

---

## Authentication

All endpoints require a valid Supabase JWT in the `Authorization: Bearer <token>` header.

The frontend (using Supabase Auth) automatically includes this token. The backend verifies it using the `SUPABASE_JWT_SECRET`.

---

## Frontend Integration

To connect the existing frontend pages to this backend:

### CodingInterviewPage — replace `setTimeout` mocks:

```ts
// Start interview
const res = await fetch('/interview/start', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${session.access_token}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({ interview_type: 'coding', question_id: selectedQuestion.id })
});
const { session_id, first_question } = await res.json();

// Send message
const msgRes = await fetch('/interview/message', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${session.access_token}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({ session_id, user_message: chatInput })
});
const { message } = await msgRes.json();

// Submit code
const submitRes = await fetch('/interview/submit-code', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${session.access_token}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({ session_id, language, code })
});
```

### Run code against test cases:

```ts
const runRes = await fetch('/ai/code/run', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${session.access_token}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({ language, code, test_cases: question.testCases })
});
const { passed_tests, total_tests, results } = await runRes.json();
```

---

## Deployment (Railway / Render)

1. Push code to GitHub
2. Connect repo to Railway or Render
3. Set all environment variables in the dashboard
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Run seed script once via console: `python seed_questions.py`

---

## MCP Tools

The backend implements MCP-style tools that the AI can conceptually call:

- **`question_tool`** — fetch questions by type/difficulty
- **`code_runner`** — sandbox execution of Python, JS, C++
- **`analytics_tool`** — user history and performance metrics

These are invoked directly by the service layer. To expose them as a proper MCP server for Claude Desktop or Claude API tool use, wrap them in an HTTP MCP server and register the tool descriptors (see `*_TOOL_DESCRIPTOR` in each tool file).
