# AI Interview Assistant Project

## Overview
This project is an AI-powered technical interview simulator. It contains a full-stack application divided into a frontend (React/Vite) and a backend (FastAPI).

### 1. Frontend
Built using Vite, React, TypeScript, shadcn-ui, and Tailwind CSS.
- **Location:** `Frontend /` directory
- **Server:** Runs on port `8080` in development (as configured in `vite.config.ts`).
- **State/Auth:** Uses Supabase for authentication and session management.

### 2. Backend
Built using FastAPI, PostgreSQL (SQLAlchemy + Alembic), and Auth via Supabase JWT verification.
- **Location:** `backend/` directory
- **Server:** Runs on port `8000` via Uvicorn.
- **APIs:** Provides endpoints for interview session management, questions, AI code evaluation, and analytics.

---

## How Data is Saved
Data persistence relies on two main services:

1. **Authentication (Supabase):**
   - User identities, logins, and JWT token issuance are managed by Supabase.
   - The frontend communicates directly with Supabase via the `VITE_SUPABASE_URL` and `VITE_SUPABASE_PUBLISHABLE_KEY` defined in `Frontend /.env`.
   - The backend validates these JWT tokens using the `SUPABASE_JWT_SECRET` defined in `backend/.env`.

2. **Application Data (PostgreSQL):**
   - **User Accounts:** Mirrored from Supabase or independently stored in the backend to attach application-specific data.
   - **Interviews:** Sessions, metadata, and user messages are logged to `interview`, `message`, and `submission` tables.
   - **Questions & Analytics:** Interview questions and user performance metrics are stored and managed by the FastAPI backend via SQLAlchemy ORM.
   - *Note: To connect to a database, populate exactly the `DATABASE_URL` field in the backend's `.env` (it defaults to a local PostgreSQL instance).*

---

## API & Architecture

The backend exposes several modular API sets (grouped by controllers):

1. **Interview Sessions API (`/interview/*`)**
   - `POST /interview/start`: Initializes a new session.
   - `POST /interview/message`: Chat interactions (fetches response from Anthropic/OpenAI).
   - `POST /interview/submit-code`: Sends the user's solution.
   - `GET /interview/report/{session_id}`: Compiles post-interview evaluation metrics.

2. **Questions API (`/questions/*`)**
   - Exposes CRUD operations to list existing questions (e.g., algorithmic, system design) and filter by difficulty.

3. **AI Code Execution API (`/ai/*`)**
   - `POST /ai/code/run`: Takes arbitrary Python/JS/C++ code, runs test cases inside a sandbox (or subprocess bounded by `SANDBOX_TIMEOUT`), and returns results.
   - Evaluates performance via AI tools wrapping `services/ai_service.py`.

*To interact with these APIs, the frontend must attach the user's Supabase JWT as a Bearer token in the `Authorization` header (`Authorization: Bearer <token>`). Currently, the frontend components (`CodingInterviewPage`, etc.) contain mock timeouts and are ready to be integrated with these endpoints.*

---

## Configuration & Environment Variables

We have linked the configuration of the Backend to match the Frontend.

### Frontend Configurations
Defined in `Frontend /.env`:
```env
VITE_SUPABASE_PROJECT_ID="pqghmairtnoylmuetcyv"
VITE_SUPABASE_PUBLISHABLE_KEY="..."
VITE_SUPABASE_URL="https://pqghmairtnoylmuetcyv.supabase.co"
```

### Backend Configurations
We populated a `backend/.env` file that bridges the gap.
1. The **`SUPABASE_URL`** has been correctly matched to the frontend Project ID `pqghmairtnoylmuetcyv`.
2. The **`CORS_ORIGINS`** list explicitly permits `http://localhost:8080`, allowing the frontend to securely make cross-origin API calls without CORS blocks.

*To ensure full operability, the following sensitive placeholders in `backend/.env` need your actual credentials:*
- `DATABASE_URL`
- `SUPABASE_JWT_SECRET` (Fetch from Supabase Dashboard -> Project Settings -> API)
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`

---

## Running the Application

### Running Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed_questions.py  # Run once to seed local Database
uvicorn app.main:app --reload --port 8000
```

### Running Frontend
```bash
cd "Frontend "
npm install
npm run dev
```

*Frontend will run on `localhost:8080` and interface with backend `localhost:8000`.*
