# Orion — Multi-Agent Workflow Orchestration Platform

A portfolio demo that shows how workflows can be orchestrated across specialized agents using a typed DAG, retry/fallback logic, approval gates, and observability.

## Recruiter-Facing Summary
Orion is a full-stack portfolio project focused on orchestration design, not model hype. The backend coordinates planner/worker/reviewer roles, tracks workflow state in SQL, and exposes APIs for runs, approvals, memory, and audit events. The frontend visualizes run status, dependency graphs, and execution traces so recruiters can quickly evaluate systems-thinking and implementation depth.

## What This Project Demonstrates
- Multi-agent coordination patterns across planner, worker, and reviewer roles.
- Deterministic workflow execution with dependency-aware scheduling.
- Retry policies, fallback actions, and approval-gated sensitive steps.
- Auditable run timelines and metrics surfaced through API + UI.
- **Agent honesty statement:** Agent routing and tool dispatch are implemented as deterministic stubs that simulate multi-agent coordination patterns; swap in a real LLM router for dynamic behavior.

## Tech Stack
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.x, Pydantic
- **Frontend:** React 18, TypeScript, Vite
- **Data:** PostgreSQL (compose), SQLite for tests/demo flows
- **Testing/quality:** pytest, Ruff, ESLint, GitHub Actions

## Architecture Overview
See [`docs/architecture.md`](docs/architecture.md) for component diagrams and service boundaries.

High-level flow:
1. Planner decomposes a goal into typed steps with dependencies.
2. Engine schedules dependency-ready steps.
3. Worker executes tool actions through a registry of deterministic tools.
4. Reviewer/approval flow can block and resume sensitive steps.
5. Audit + metrics are persisted for replay and analysis.

## How to Run Locally
### Option A: Docker Compose
```bash
docker compose up --build
```
- API docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

### Option B: Native
```bash
# backend
cd backend
pip install -e .[dev]
ORION_JWT_SECRET=dev-secret uvicorn app.main:app --reload --port 8000

# frontend (new shell)
cd frontend
npm ci
npm run dev
```

## Demo Workflow
```bash
python scripts/run_sample_workflow.py \
  --goal "Search the vendor landscape. Then compare three options. Summarize findings."
```
The sample runner submits a workflow and prints step-by-step execution history using the deterministic agent/tool simulation.

## Screenshots / Demo
- Screenshot catalog: [`docs/screenshots/README.md`](docs/screenshots/README.md)
- Portfolio Preview page: [`docs/preview/index.html`](docs/preview/index.html)
- UI/Design preview link: [Perplexity Portfolio Preview](https://www.perplexity.ai/computer/a/orion-preview-project-1-of-9-lCA5DWRgQoa4AN6VYPXAUQ)

## Limitations and Future Work
- Current agents/tools are deterministic stubs, not live LLM-driven routing.
- Token/cost accounting is not implemented because no live model calls are active.
- Tool integrations (real web search, hardened sandbox, external services) are still demo-scale.
- Future version can replace planner routing with an LLM-backed router and real embeddings.

## Resume Bullets
See [`docs/resume-bullets.md`](docs/resume-bullets.md).

## License
This project is licensed under the terms in [`LICENSE`](LICENSE).
