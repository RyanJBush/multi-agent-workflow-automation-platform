# Resume Bullets — Orion

- Built a FastAPI + SQLAlchemy orchestration backend that decomposes user goals into typed DAG steps and executes dependency-aware runs.
- Implemented planner, worker, and reviewer agent roles with explicit handoffs and structured run traces across API and UI.
- Added deterministic tool routing (search/math/http/code stubs) to demonstrate multi-agent coordination without external model dependencies.
- Designed retry policies, fallback actions, and approval-gated sensitive steps to model realistic orchestration control flow.
- Developed React + TypeScript interface views for DAG visualization, run logs, metrics, approvals, and agent/tool status.
- Exposed versioned REST endpoints for workflows, tasks, approvals, memory, audit events, and usage records.
- Wrote pytest coverage for planner decomposition, workflow retries/fallbacks, approval handling, and lifecycle state transitions.
- Packaged local developer workflows with Make targets and Docker Compose for quick setup and repeatable demos.
