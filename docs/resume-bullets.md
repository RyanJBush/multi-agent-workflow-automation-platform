# Resume Bullets — Orion (Multi-Agent Workflow Orchestration Platform)

ATS-friendly, single-line bullets. Pick 3–5 that best match the role.

## Headline bullets

- Built a multi-agent workflow orchestration platform in Python and FastAPI that decomposes user goals into a typed DAG and routes steps across role-specialized planner, worker, and reviewer agents.
- Designed an agent contract layer (request, response, reasoning trace) so every step emits a structured decision log usable by the API, the UI, and the audit trail.
- Implemented a DAG executor with topological scheduling, parallel branch execution, per-step retry with exponential backoff, and fallback action routing on timeout or runtime failure.
- Added a human-in-the-loop approval gate that pauses sensitive tool calls until a reviewer decision is recorded, with full audit logging of who approved what and when.
- Built a tool registry pattern with permission checks, schemas, and timeouts so new tools (search, HTTP, code execution, math) can be added without modifying the orchestrator.
- Modeled workflow state as a state machine over SQLAlchemy persistence (`pending → running → blocked/completed/failed`) with replay and pause/resume endpoints.
- Wrote 129 pytest unit and API tests covering planner decomposition, retry behavior, approvals, audit, memory, and end-to-end workflow runs; integrated GitHub Actions CI for lint + tests.
- Shipped a React + TypeScript + Vite dashboard that visualizes the agent graph, run timeline, per-step logs, and approval queue for in-flight workflows.

## Skill-anchored variants

- AI agents: Designed role-specialized planner, worker, and reviewer agents with scoped tool access and structured reasoning traces logged per decision.
- Multi-agent systems: Implemented task routing across named agents based on instruction parsing and tool capability, with fallback agent selection on failure.
- Workflow orchestration: Built a DAG executor with topological scheduling, parallel branch execution, and pause/resume/replay semantics over a state machine.
- Automation: Modeled five end-to-end automation scenarios (research, triage, reporting, retry, approval) runnable from a single CLI script.
- APIs: Designed a versioned FastAPI surface (`/api/v1/workflows`, `/tasks`, `/approvals`, `/memory`) with Pydantic schemas and OpenAPI docs.
- State management: Tracked workflow and step state in SQLAlchemy with explicit transitions, audit events, and timeline reconstruction.
- Task routing: Wrote a planner that maps natural-language instructions to typed actions (`search`, `http_request`, `math`, `code_exec`, `echo`) and selects the right worker.

## One-liner (portfolio site)

> Orion — a Python and FastAPI platform that routes a user goal across role-specialized AI agents on a DAG, with retries, approval gates, and a React dashboard.
