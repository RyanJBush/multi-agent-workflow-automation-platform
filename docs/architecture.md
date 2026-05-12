# Orion Architecture

Orion is a multi-agent workflow orchestration platform that decomposes a user
goal into a typed DAG and executes it through role-specialized agents and a
tool registry. This document describes the runtime, the persistence model,
and the boundaries between components.

> **Scope note.** Tool execution is intentionally deterministic — there is no
> live LLM call and no external network egress. The orchestration patterns
> (planning, routing, retries, fallback, approvals, replay) are real; the
> tool implementations are stubs. See
> [Limitations](../README.md#-limitations--future-work).

---

## 1. Components

| Component | Location | Responsibility |
|---|---|---|
| `PlannerAgent` | `backend/app/agents/planner_agent.py` | Decomposes a goal into ordered `PlannedStep`s with dependencies, retry policy, fallback action |
| `WorkerAgent` (general + math) | `backend/app/agents/worker_agent.py` | Executes a step by invoking the named tool from the registry |
| `ReviewerAgent` | `backend/app/agents/reviewer_agent.py` | Reviews completed steps and surfaces a structured reasoning trace |
| `WorkflowEngine` | `backend/app/services/workflow_engine.py` | Drives DAG execution, persists step state, applies retries/fallbacks, gates sensitive steps on approvals |
| `ToolRegistry` | `backend/app/tools/registry.py` | Single point of dispatch for tool invocations; enforces per-tool timeouts |
| Tools | `backend/app/tools/default_tools.py` | Deterministic stubs (`echo`, `math`, `search`, `http_request`, `code_exec`, `flaky`, `slow_echo`, `sensitive_echo`) |
| `MemoryService` | `backend/app/services/memory_service.py` + `memory.py` | Basic key/value memory + FAISS vector store using `FakeEmbeddings` |
| `ApprovalService` | `backend/app/services/approval_service.py` | Records human-in-the-loop decisions and unblocks paused runs |
| `AuditService` | `backend/app/services/audit_service.py` | Append-only audit log of run-level events |
| `UsageService` | `backend/app/services/usage_service.py` | Per-actor quota tracking (call-count limits; not token cost) |
| `WorkflowInsightService` | `backend/app/services/workflow_insight_service.py` | Generates plan explanation, quality score, reflection, suggestions from persisted run state |
| API routers | `backend/app/api/routers/*.py` | Versioned HTTP surface under `/api/v1` |
| Frontend | `frontend/src/` | React + TypeScript SPA with dashboard, tasks, workflow execution, agent monitor, settings, demo pages |

## 2. Runtime flow

```
POST /api/v1/tasks/submit
  └── TaskService creates Task + WorkflowRun (status=pending)
        └── PlannerAgent.decompose(title, description)
              → list[PlannedStep]  (id, owner, action, dependencies, retry_policy, fallback_action)
        └── WorkflowEngine.execute_run(run_id)
              ├── for each step in topological order:
              │     ├── if action ∈ {sensitive_echo, ...}: status=blocked, await /approvals decision
              │     ├── invoke worker.execute(action, instruction, timeout_seconds)
              │     │     └── tool_registry.run(name, worker_name, input_text, timeout_override)
              │     ├── on timeout/runtime error: apply RetryPolicy (max_retries, backoff)
              │     ├── if retries exhausted and fallback_action set and error matches fallback_on_errors:
              │     │     └── invoke fallback action (e.g. echo)
              │     └── persist ExecutionStep (status, latency, output, retry count, fallback marker)
              └── compute run-level status (completed / failed / blocked / cancelled)
```

The planner is **keyword-based, not LLM-driven**. `decompose()` splits the
goal on `.` and `;`, scans each chunk for routing tokens (`search`,
`vendor`, `compare`, `kpi`, `incident`, `sensitive`, `flaky`, etc.), and
picks a tool + worker accordingly. This is intentional: it keeps the planner
deterministic for tests and demos while preserving the structural shape
(`PlannedStep` with dependencies + retry + fallback) that a real
LLM-based planner would emit.

## 3. Backend layering

```
app/
├── main.py                  # FastAPI app factory + startup hooks
├── api/
│   ├── router.py            # mounts versioned router under /api/v1
│   └── routers/             # one file per domain (tasks, workflows, agents, tools,
│                            #   approvals, memory, audit, usage)
├── services/                # orchestration + domain logic
│   ├── workflow_engine.py   # DAG execution + retry/fallback + approval gates
│   ├── task_service.py
│   ├── workflow_service.py
│   ├── workflow_template_service.py
│   ├── workflow_insight_service.py
│   ├── memory_service.py / memory.py
│   ├── approval_service.py
│   ├── audit_service.py
│   ├── usage_service.py
│   ├── orchestration_service.py
│   ├── agent_service.py
│   └── tools.py
├── repositories/            # SQLAlchemy persistence boundaries
├── agents/
│   ├── contracts.py         # AgentRequest / AgentResponse / ReasoningTrace
│   ├── planner_agent.py
│   ├── worker_agent.py
│   └── reviewer_agent.py
├── tools/
│   ├── base.py              # Tool interface
│   ├── registry.py          # registration + dispatch + timeout enforcement
│   └── default_tools.py     # echo, math, search, http_request, code_exec, flaky, ...
├── models/                  # SQLAlchemy tables (also legacy models.py)
├── schemas/                 # Pydantic request/response shapes
├── db/                      # engine, session, base, init
└── core/                    # config, security, settings
```

## 4. Data model (persisted entities)

| Table | Purpose |
|---|---|
| `tasks` | The user-submitted goal (title + description + scenario tag) |
| `workflow_runs` | A single execution instance of a task; carries `status`, `trace_id`, timestamps |
| `execution_steps` | Per-step state: `action`, `instruction`, `dependencies`, `status`, `output`, retry count, fallback marker, latency |
| `workflow_templates` | Saved workflows that can be re-run on demand |
| `approvals` | Pending and decided approval records, tied to a run + step |
| `audit_events` | Append-only log of run-level transitions |
| `memory_entries` | Basic key/value memory with namespaces and correction support |
| `vector_memory` | FAISS-backed embedding rows (built with `FakeEmbeddings`) |
| `usage_quotas` | Per-actor call-quota records (not token cost) |
| `agents` | Registered agent records surfaced through `/agents` |

## 5. Tool registry pattern

Tools implement a simple contract:

```python
class Tool:
    name: str
    def run(self, input_text: str) -> str: ...
```

The registry stores instances by name and exposes a single
`run(name, worker_name, input_text, timeout_override)` entry point. Adding
a new tool means writing a class, registering it, and (optionally) teaching
the planner to route to it — the engine itself does not change.

The current tools are all deterministic:

- `echo` — returns input.
- `math` — sums numeric tokens in the input.
- `search` — keyword lookup against an in-process corpus (no HTTP).
- `http_request` — returns canned JSON for whitelisted mock paths (no HTTP).
- `code_exec` — evaluates an AST-validated arithmetic expression; arbitrary
  code is rejected by both a regex and an AST-node allowlist.
- `flaky` — fails on first attempt, succeeds on retry (failure-injection
  helper for tests).
- `slow_echo` — sleeps before returning (timeout-injection helper).
- `sensitive_echo` — used by the approval-gate test path.

## 6. Retry, fallback, and approval gates

- **Retry.** Each `PlannedStep` carries a
  `RetryPolicy(max_retries, backoff_seconds)`. The engine retries on
  `timeout` and `runtime` errors with exponential-style backoff.
- **Fallback.** A step may declare `fallback_action="echo"` and
  `fallback_on_errors=["timeout", "runtime"]`. If the primary tool exhausts
  its retries and the error matches, the fallback is invoked and the step is
  marked `completed` with a `fallback` flag.
- **Approval gates.** When the planner classifies a chunk as sensitive
  (tokens like `sensitive`, `approve`, `approval`, `export`), the step is
  routed to `sensitive_echo`. The engine pauses the run in `blocked` until
  a decision is recorded via `POST /approvals/{approval_id}/decision`.

## 7. Observability

- **Per-run metrics** (`GET /workflows/runs/{run_id}/metrics`):
  `total_steps`, `completed_steps`, `failed_steps`, `retried_steps`,
  `fallback_steps`, `avg_step_latency_ms`.
- **Platform metrics** (`GET /workflows/metrics`): `total_runs`,
  `completion_rate`, `retry_rate`, `avg_step_latency_ms`,
  `run_status_counts`, `tool_reliability`.
- **Timeline** (`GET /workflows/runs/{run_id}/timeline`): the ordered event
  log for a single run.
- **Insights** (`GET /workflows/runs/{run_id}/insights`): a generated plan
  explanation, reflection, and suggested next actions, computed from the
  persisted run state.
- **Audit log** (`POST /audit`, `GET /audit`): append-only record of
  run-level events.

> **Token cost is not tracked.** Run-level latency and retry/fallback counts
> are the cost signals today; per-token accounting is reserved for the
> point at which a real LLM is integrated.

## 8. Frontend

- `src/App.tsx` mounts the React Router tree.
- Pages: `DashboardPage`, `TasksPage`, `WorkflowExecutionPage`,
  `AgentMonitorPage`, `SettingsPage`, `DemoPage`.
- Workflow visualization lives in `src/components/workflow/`:
  `WorkflowGraph.tsx`, `WorkflowSteps.tsx`, `ExecutionLogPanel.tsx`.
- API access is centralized in `src/services/api.ts`.

## 9. Testing

129 tests in `backend/tests/` cover:

- Tool registry + planner branching (`test_tools_and_planner.py`).
- Retry exhaustion and fallback selection (`test_workflow_retries.py`).
- Approval-gate state transitions (`test_approvals.py`).
- Audit log behavior (`test_audit.py`).
- Memory write/search (`test_memory.py`).
- Usage quotas (`test_usage.py`).
- End-to-end task → run → completion (`test_tasks_workflow.py`).
- Service-level edge cases (`test_unit_coverage.py`,
  `test_metrics_and_planner_coverage.py`,
  `test_workflow_insight_service.py`,
  `test_task_service_and_session.py`,
  `test_additional_api_coverage.py`,
  `test_health.py`).

Run with `make test` or `cd backend && PYTHONPATH=. pytest`.
