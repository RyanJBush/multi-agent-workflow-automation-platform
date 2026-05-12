# Orion Demo Runbook

A two-minute walkthrough for recruiters and reviewers. Run these in order to
see the orchestration patterns end-to-end without needing any external API
keys.

> **Prerequisites:** Python 3.11+, Node 20+ (only for the UI path), Docker
> (only for the docker-compose path). No LLM keys required — tools are
> deterministic stubs.

---

## Path A — CLI only (fastest, ~60 seconds)

This boots the FastAPI app in-process against an ephemeral SQLite DB. No
Docker, no frontend.

```bash
# 1. Install backend deps (one time)
cd backend && pip install -e .[dev] && cd ..

# 2. Run the default research scenario
python scripts/run_sample_workflow.py
```

Expected output (truncated):

```
[orion-demo] submitting goal: 'Search the vendor landscape. Then compare three options. Summarize findings.'
[orion-demo] run_id=1 initial_status='pending'
[orion-demo] run status: running
[orion-demo] run status: completed
[orion-demo] timeline (truncated):
{
  "events": [
    {"step_id": "step-1", "action": "search",  "status": "completed", ...},
    {"step_id": "step-2", "action": "search",  "status": "completed", ...},
    {"step_id": "step-3", "action": "echo",    "status": "completed", ...}
  ]
}
[orion-demo] final status: completed
```

### Try the other scenarios

```bash
# Retry + fallback path — the flaky tool fails then recovers
python scripts/run_sample_workflow.py \
  --goal "Run the flaky integration probe. If it times out, fall back to a simple echo."

# Human-in-the-loop — run will end in 'blocked' awaiting approval
python scripts/run_sample_workflow.py \
  --goal "Export the sensitive customer extract. This step requires explicit human approval."

# Math + http_request mix
python scripts/run_sample_workflow.py \
  --goal "Fetch the api/kpi snapshot. Compute the sum of the values. Summarize."
```

All five scenarios are catalogued in
[`data/sample_tasks.json`](../data/sample_tasks.json).

### What to point out

- `step-N` IDs and `dependencies` — proof the DAG is real data, not a fiction.
- Each step's `action` (`search`, `math`, `http_request`, `flaky`, …) — proof
  the planner is routing to tools, not just running one big LLM call.
- `retried_steps` and `fallback_steps` in
  `GET /api/v1/workflows/runs/{run_id}/metrics` — proof retry + fallback
  fired.
- A `blocked` run on the sensitive-export scenario — proof the approval
  gate halts execution.

---

## Path B — Full stack via Docker Compose

```bash
docker compose up --build
# Backend API docs: http://localhost:8000/docs
# Frontend:         http://localhost:5173
```

Walkthrough:

1. Open `http://localhost:8000/docs` → expand `tasks/submit` → click
   **Try it out** → submit a goal. (Auto-generated OpenAPI surface.)
2. Open `http://localhost:5173/`.
   - **Dashboard** — KPI cards for completion rate, retry rate, latency.
   - **Tasks** — submit and list tasks.
   - **Workflow Execution** — DAG view, step timeline, execution log.
   - **Agent Monitor** — planner / worker / reviewer status.
3. From the Workflow Execution page, watch a run move from
   `pending → running → completed` (or `blocked` for the approval scenario).
4. From the API docs, hit `GET /workflows/runs/{id}/metrics` and
   `/timeline` for the run you just saw in the UI.

---

## Path C — Inspect the API surface only

```bash
# Backend native dev loop
cd backend
ORION_JWT_SECRET=dev-secret uvicorn app.main:app --reload --port 8000

# In another shell, seed and call the API:
curl -X POST http://localhost:8000/api/v1/workflows/templates/seed-demo
curl http://localhost:8000/api/v1/workflows/metrics
curl http://localhost:8000/api/v1/tools/registry
```

---

## Path D — Run the test suite

The orchestration patterns are most convincing in the test suite:

```bash
cd backend && PYTHONPATH=. pytest -q
# 129 tests covering planner branching, retries, fallback, approvals,
# audit, memory, usage, and end-to-end run lifecycle.
```

Highlights for a reviewer:

- `tests/test_workflow_retries.py` — retry + fallback behavior.
- `tests/test_approvals.py` — `blocked` state + approval-decision flow.
- `tests/test_tools_and_planner.py` — planner-to-tool routing.
- `tests/test_tasks_workflow.py` — end-to-end task submission.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ImportError: app.main` from `scripts/run_sample_workflow.py` | Run from the repo root, not from inside `scripts/` |
| `JWT secret not configured` | Set `ORION_JWT_SECRET=anything` in the env |
| `docker compose` build slow on first run | The langchain wheel is heavy; subsequent builds are cached |
| Frontend won't talk to backend | Confirm `VITE_API_BASE_URL` is `http://localhost:8000/api/v1` |
