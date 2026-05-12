# Resume Bullets — Orion (Multi-Agent Workflow Orchestration Platform)

ATS-friendly, single-line bullets. Each statement is grounded in code or
tests in this repo. Pick the 5–8 that best match the target role.

> **Honest framing.** This is a portfolio project. Tool calls are
> deterministic stubs (no live LLM, no external APIs). The orchestration,
> retry/fallback, approval, and observability patterns are real and tested.

---

## Top 8 ATS bullets (recommended set)

- Built a multi-agent workflow orchestration platform in Python and FastAPI that decomposes a user goal into a typed DAG and routes steps across role-specialized planner, worker, and reviewer agents.
- Designed a typed agent contract (request, response, structured reasoning trace) so every step in a run emits an auditable decision record consumed by the API, the UI, and the audit log.
- Implemented a DAG executor with topological scheduling, parallel branch execution via `ThreadPoolExecutor`, per-step retry with exponential-style backoff, and configurable fallback action routing on timeout or runtime failure.
- Added a human-in-the-loop approval gate that pauses sensitive steps in a `blocked` state until a reviewer decision is recorded via the approvals API, with full audit logging.
- Built a tool registry pattern with per-tool timeouts and a uniform `Tool` interface so new tools can be added without modifying the orchestrator; ships with eight deterministic tools (echo, math, search, http_request, code_exec, plus failure-injection helpers).
- Modeled workflow state as a state machine over SQLAlchemy 2.x (`pending → running → blocked / completed / failed / cancelled`) with pause, resume, cancel, and replay endpoints.
- Shipped a React 18 + TypeScript + Vite dashboard that visualizes the agent graph, run timeline, per-step execution log, approval queue, and platform-level KPI cards.
- Wrote 129 pytest unit and API tests covering planner decomposition, retry/fallback behavior, approval flow, audit, memory, and end-to-end runs; wired GitHub Actions CI for ruff lint, mypy (advisory), pytest, and frontend lint + build.

---

## Skill-anchored variants (drop-in replacements)

- **AI agents** — Designed role-specialized planner, worker, and reviewer agents with scoped tool access and structured reasoning traces persisted per decision.
- **Multi-agent systems** — Implemented task routing across named agents based on instruction parsing and tool capability, with fallback agent selection on failure.
- **Workflow orchestration** — Built a DAG executor with topological scheduling, parallel branch execution, and pause / resume / replay semantics over a SQLAlchemy state machine.
- **Automation** — Modeled five end-to-end automation scenarios (research, triage, reporting, retry, approval) runnable from a single CLI script with no API keys required.
- **APIs** — Designed a versioned FastAPI surface (`/api/v1/tasks`, `/workflows`, `/approvals`, `/memory`, `/audit`, `/usage`) with Pydantic schemas and auto-generated OpenAPI docs.
- **State management** — Tracked workflow and step state in SQLAlchemy with explicit transitions, audit events, and a timeline reconstruction endpoint.
- **Task routing** — Wrote a planner that maps natural-language instructions to typed actions (`search`, `http_request`, `math`, `code_exec`, `echo`) and selects the appropriate worker.
- **Observability** — Exposed per-run and platform-level metrics (completion rate, retry rate, fallback rate, avg step latency, tool reliability) via dedicated `/metrics` endpoints.
- **Testing** — Drove development with 129 pytest tests across API, planner, retries, fallbacks, approvals, memory, and audit; integrated CI on every push.
- **Containerization** — Provided a Docker Compose stack (FastAPI + Postgres 16 + Vite frontend) plus a Makefile-driven local dev loop.

---

## One-liner (portfolio site / LinkedIn headline)

> **Orion** — a Python + FastAPI portfolio platform that routes a user goal across role-specialized AI agents on a DAG, with retries, fallbacks, approval gates, run metrics, and a React + TypeScript dashboard. 129 tests, CI green.
