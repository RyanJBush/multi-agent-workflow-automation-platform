# Resume Bullets — Orion

- Built a FastAPI + SQLAlchemy orchestration backend that decomposes user goals into typed DAG steps and executes dependency-aware workflow runs.
- Designed planner, worker, and reviewer agent contracts with structured reasoning traces to keep run decisions auditable across API and UI surfaces.
- Implemented deterministic tool routing (search/math/http/code stubs) to simulate multi-agent coordination patterns without external model dependencies.
- Added retry policies, fallback actions, and approval-gated sensitive steps to model realistic workflow control behavior in a demo-scale system.
- Developed React + TypeScript dashboard views for workflow DAGs, run logs, KPI metrics, and approval queue monitoring.
- Exposed versioned REST endpoints for tasks, workflows, approvals, memory, audit events, and usage tracking with Pydantic-typed request/response schemas.
- Wrote pytest coverage across planner decomposition, retries/fallbacks, approvals, memory, and run lifecycle transitions.
- Packaged local developer workflows with Docker Compose, Make targets, and CI checks for linting and test execution.
