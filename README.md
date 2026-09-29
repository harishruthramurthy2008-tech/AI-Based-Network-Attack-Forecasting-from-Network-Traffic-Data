# WhetherGPT

WhetherGPT is an AI-powered conversational weather application built with FastAPI, React, and PostgreSQL.

## Run locally

```bash
cd backend
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Docker:

```bash
docker compose up --build
```
