# Orion API

Base path: **`/api/v1`** — Auto-generated OpenAPI docs are served at
`http://localhost:8000/docs` once the backend is running. The endpoints below
are derived directly from `backend/app/api/routers/`; if you spot a drift,
the routers are the source of truth.

> **Authentication.** JWT bearer auth is plumbed through
> `app/core/security.py`. The demo CLI sets a static `ORION_JWT_SECRET` so
> the routes can be exercised without a full identity flow.

---

## Health

| Method | Path | Description |
|---|---|---|
| `GET` | `/healthz` | Liveness probe; returns `{"status":"ok"}` |

## Tasks

| Method | Path | Description |
|---|---|---|
| `GET` | `/tasks` | List tasks |
| `POST` | `/tasks` | Create a task without running it |
| `GET` | `/tasks/{task_id}` | Fetch one task |
| `POST` | `/tasks/submit` | Create task + planner run + execute (primary entry point) |
| `POST` | `/tasks/enqueue` | Queue a task for later dispatch |
| `POST` | `/tasks/dispatch-next` | Pop the next queued task and execute it |

Example — submit a goal:

```bash
curl -X POST http://localhost:8000/api/v1/tasks/submit \
  -H 'Content-Type: application/json' \
  -d '{"title":"Vendor research","description":"Search the vendor landscape. Then compare three options. Summarize."}'
```

## Workflows

| Method | Path | Description |
|---|---|---|
| `GET` | `/workflows` | List workflow runs |
| `POST` | `/workflows` | Create a workflow run |
| `GET` | `/workflows/templates` | List saved workflow templates |
| `POST` | `/workflows/templates` | Save a template |
| `POST` | `/workflows/templates/seed-demo` | Seed built-in demo templates |
| `POST` | `/workflows/templates/{template_id}/run` | Execute a saved template |
| `GET` | `/workflows/runs/{run_id}` | Fetch a run with step state |
| `GET` | `/workflows/runs/{run_id}/timeline` | Ordered event log for a run |
| `GET` | `/workflows/runs/{run_id}/metrics` | Step counts, retries, fallbacks, avg latency |
| `GET` | `/workflows/runs/{run_id}/insights` | Generated plan explanation + reflection + suggestions |
| `POST` | `/workflows/runs/{run_id}/pause` | Pause an in-flight run |
| `POST` | `/workflows/runs/{run_id}/resume` | Resume a paused run |
| `POST` | `/workflows/runs/{run_id}/cancel` | Cancel a run |
| `POST` | `/workflows/runs/{run_id}/replay` | Replay a completed run as a new run |
| `GET` | `/workflows/metrics` | Platform-level run metrics |

### Per-run metrics shape

```json
{
  "run_id": 7,
  "trace_id": "tr_…",
  "total_steps": 3,
  "completed_steps": 3,
  "failed_steps": 0,
  "retried_steps": 1,
  "fallback_steps": 0,
  "avg_step_latency_ms": 12.4
}
```

### Platform metrics shape

```json
{
  "total_runs": 42,
  "completion_rate": 0.93,
  "retry_rate": 0.18,
  "avg_step_latency_ms": 11.8,
  "run_status_counts": {"completed": 39, "failed": 2, "blocked": 1},
  "tool_reliability": [{"tool": "search", "success_rate": 1.0, "calls": 20}]
}
```

> **Cost endpoint.** There is **no** `/cost` endpoint today — Orion does not
> yet integrate a real LLM, so per-token cost is not measured. Use
> `/workflows/runs/{id}/metrics` for latency + retry signals and `/usage`
> for per-actor quotas.

## Agents

| Method | Path | Description |
|---|---|---|
| `GET` | `/agents` | List registered agents (planner, worker, reviewer) |
| `POST` | `/agents` | Register an agent record |

## Tools

| Method | Path | Description |
|---|---|---|
| `GET` | `/tools/registry` | List tools registered with the tool registry |
| `GET` | `/tools/health` | Tool registry health |

The tools listed by `/tools/registry` are all deterministic stubs
(`echo`, `math`, `search`, `http_request`, `code_exec`, `flaky`, `slow_echo`,
`sensitive_echo`). See
[`docs/architecture.md`](architecture.md#5-tool-registry-pattern).

## Approvals (human-in-the-loop)

| Method | Path | Description |
|---|---|---|
| `POST` | `/approvals` | Create an approval request for a blocked step |
| `POST` | `/approvals/{approval_id}/decision` | Approve or reject |
| `GET` | `/approvals/runs/{run_id}` | List approvals for a run |

## Memory

| Method | Path | Description |
|---|---|---|
| `POST` | `/memory/basic/write` | Write to key/value memory |
| `POST` | `/memory/vector/write` | Write to FAISS vector memory |
| `POST` | `/memory/vector/search` | Cosine-similarity search |
| `POST` | `/memory/basic/{entry_id}/correct` | Correct a stored entry |
| `GET` | `/memory/summary/{namespace}` | Summary of entries in a namespace |

> Embeddings use `langchain-community.FakeEmbeddings` so the vector path
> works without any external API key.

## Audit

| Method | Path | Description |
|---|---|---|
| `POST` | `/audit` | Append an audit event |
| `GET` | `/audit` | List audit events |

## Usage

| Method | Path | Description |
|---|---|---|
| `GET` | `/usage/quota/{actor_id}` | Read quota for an actor |
| `POST` | `/usage/quota` | Set quota for an actor |

`/usage` covers call-count quotas only — it is not a token-cost meter.
