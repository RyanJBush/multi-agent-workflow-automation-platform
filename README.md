# Multi-Agent Workflow Automation Platform

## Executive Summary
This project is a recruiter-ready demonstration of a **multi-agent workflow automation platform** for AI engineering and software automation use cases. It shows how a Python backend can decompose a user goal into dependency-aware steps, route each step to role-based agents, execute tool calls through a registry, and persist execution state for replay and analysis. The implementation emphasizes orchestration system design (planning, routing, retries, approvals, observability) with deterministic agents/tools rather than external LLM APIs.

## Workflow Automation Problem This Project Solves
Teams often have repeatable multi-step tasks (research, analysis, review, approvals) but no consistent orchestration layer to:
- break high-level goals into executable steps,
- route work to the right agent role,
- handle failures with retries/fallbacks,
- pause on sensitive actions for human approval,
- and provide auditable run history and metrics.

This platform implements that orchestration layer end to end through API + UI so workflows are structured, traceable, and repeatable.

## Key Features
- **Goal-to-workflow decomposition:** planner converts task text into ordered DAG-like execution steps with dependencies.
- **Role-based agent flow:** planner, worker, and reviewer agents each have clear responsibilities.
- **Tool registry execution model:** workers invoke named tools through a single registry interface.
- **Reliability controls:** retry policies, timeout handling, and fallback actions per step.
- **Human-in-the-loop approvals:** sensitive steps can block execution until approval/rejection is recorded.
- **Run lifecycle controls:** pause, resume, cancel, and replay workflow runs.
- **Observability:** run timelines, run-level metrics, platform metrics, audit events, and generated workflow insights.
- **State + memory services:** persistent task/run/step storage plus basic and vector memory endpoints.

## Tech Stack
- **Backend:** Python 3.11+, FastAPI, Pydantic, SQLAlchemy.
- **Frontend:** React 18, TypeScript, Vite, React Router.
- **Data/storage:** PostgreSQL via Docker Compose (SQLite fallback in local config paths).
- **Testing & quality:** pytest, ruff, ESLint.
- **Containerization/dev workflow:** Dockerfiles, docker-compose, Makefile automation.

## Multi-Agent Architecture Overview
At runtime, task submission triggers a planner-driven workflow run:
1. **Task service** stores the task and creates a workflow run.
2. **Planner agent** decomposes the goal into structured planned steps (with dependencies/retry/fallback metadata).
3. **Workflow engine** executes dependency-ready steps in order.
4. **Worker agent** invokes the selected tool through the registry.
5. **Reviewer agent** records structured review traces.
6. **Persistence + observability services** store step status, audit events, approvals, usage quotas, and metrics/insights.

Important implementation constraint: the default agents/tools are deterministic stubs for orchestration demonstration, not live external LLM/tool integrations.

## Agent Roles and Workflow Sequence
### Agent roles
- **Planner Agent**
  - Parses goal text and creates planned steps.
  - Assigns tool/action type, owner hints, dependencies, retry/fallback settings.
- **Worker Agent**
  - Executes each step by calling a registered tool.
  - Returns outputs/errors used by retry/fallback logic.
- **Reviewer Agent**
  - Produces a structured review/trace for completed execution context.

### Workflow sequence
1. Client submits `POST /api/v1/tasks/submit` with title/description.
2. Planner produces step plan.
3. Engine persists and runs steps.
4. If a step fails, engine retries based on policy; may fallback if configured.
5. If a step is sensitive, run is blocked pending `/approvals` decision.
6. Run ends as completed/failed/blocked/cancelled; metrics, timeline, audit, and insights are queryable.

## Setup and Installation
### Prerequisites
- Python 3.11+
- Node.js 18+
- npm
- (Optional) Docker + Docker Compose

### Local setup
```bash
make setup
```

### Start backend
```bash
make dev-backend
```
Backend docs: `http://localhost:8000/docs`

### Start frontend (new terminal)
```bash
make dev-frontend
```

### Optional full stack with containers
```bash
make up
```

### Run sample orchestrated workflow
```bash
make run-orchestrator-demo
```

### Run tests
```bash
make test
```

## Example Use Cases
- **AI operations workflow simulation:** decompose a request into research/analysis/review-style steps and execute with visibility.
- **Approval-gated automation:** route sensitive actions into a blocked state until a human decision is captured.
- **Reliability testing for orchestrators:** exercise flaky/slow/sensitive tool paths to validate retry, timeout, and fallback behavior.
- **Workflow analytics demos:** inspect run metrics, timelines, and tool reliability summaries for post-run evaluation.

## Skills Demonstrated
- Multi-agent workflow orchestration design.
- Task decomposition and step dependency management.
- API-first backend architecture with modular service/repository layers.
- Deterministic tool routing via registry pattern.
- Reliability engineering patterns (retry, fallback, timeout handling).
- Human-in-the-loop control points (approvals).
- Observability design (metrics, timelines, audit logs, insights).
- Full-stack implementation and documentation for technical communication.

## Resume-Ready Project Description
Built a **Multi-Agent Workflow Automation Platform** using **Python/FastAPI** and **React/TypeScript** to orchestrate goal-driven tasks across planner, worker, and reviewer agents. Implemented dependency-aware execution, tool-registry dispatch, retry/fallback policies, approval-gated actions, and run lifecycle controls (pause/resume/cancel/replay), with persistent observability through metrics, timelines, and audit logs. Designed the system as a modular orchestration architecture suitable for extending into production LLM-integrated agent workflows.

## Future Improvements
- Replace deterministic planner/worker behavior with optional live LLM-backed planning and tool selection.
- Add production-grade authn/authz and role-based access controls for workflow operations.
- Expand tool adapter framework for real external systems (ticketing, data warehouses, internal APIs).
- Improve queueing/concurrency controls for higher-throughput execution.
- Add deeper evaluation and guardrail layers (policy checks, automated run quality scoring).
- Extend frontend with richer DAG visualization and live execution streaming.
