# Multi-Agent Workflow Automation Platform

## 1) Project Title
**Multi-Agent Workflow Automation Platform**

## 2) Executive Summary
This project showcases a full-stack, API-first orchestration platform for multi-step AI workflow automation. A FastAPI backend plans and executes dependency-aware workflows across planner, worker, and reviewer agents, while a React dashboard provides run control and visibility. The implementation focuses on reliable orchestration patterns (routing, retries, fallback, approvals, replay, observability) using deterministic demo tools and agents.

## 3) Workflow Automation Problem This Project Solves
Many engineering teams have repeatable AI/automation tasks but lack a standardized orchestration layer to break work into steps, route actions to the right agent/tool, and track execution outcomes. This project solves that by providing structured planning, run-state persistence, tool dispatch, and operational controls in one system. It turns ad hoc automation into a traceable workflow lifecycle with metrics, timeline events, and auditability.

## 4) Key Features
- Goal decomposition into ordered workflow steps with dependencies and retry policies.
- Role-based agent design (`planner`, `worker-general`, `worker-math`, `reviewer`).
- Tool registry pattern with worker/tool permissions and per-tool timeout enforcement.
- Retry, backoff, and fallback execution handling in the workflow engine.
- Human-in-the-loop approvals for sensitive tool actions.
- Run controls: pause, resume, cancel, replay (including replay from a specific step).
- Observability endpoints for run timelines, run metrics, platform metrics, and run insights.
- Audit event logging for workflow lifecycle actions.
- Usage quota enforcement per actor for task submissions.
- Memory services for basic namespace entries and vector-style retrieval (demo embedding logic).

## 5) Tech Stack
- **Backend:** Python 3.11+, FastAPI, Pydantic, SQLAlchemy
- **Frontend:** React 18, TypeScript, Vite, React Router
- **Data layer:** PostgreSQL via Docker Compose, SQLite default local fallback
- **Tooling:** pytest, Ruff, ESLint, Makefile, Docker/Docker Compose

## 6) Multi-Agent Architecture Overview
Task submission creates a workflow run and triggers planner-driven step generation. The workflow engine validates dependency structure, executes ready steps (including parallel-ready steps), and persists state transitions. Worker agents call tools through a centralized registry, reviewer agents score/validate outputs, and supporting services persist approvals, audit events, memory entries, and usage/metrics data.

> Current scope is intentionally deterministic: default tools simulate search/API/code execution behavior and do not perform real external network calls.

## 7) Agent Roles and Workflow Sequence
### Agent roles
- **Planner Agent:** parses task text, assigns step actions, worker ownership, dependencies, and retry/fallback metadata.
- **Worker Agents:** execute routed actions through the tool registry with permission and timeout constraints.
- **Reviewer Agent:** evaluates produced outputs and writes structured review metadata used in run events.

### Workflow sequence
1. Client submits a task (`/api/v1/tasks/submit` or template run).
2. Planner decomposes the goal into executable steps.
3. Engine persists steps and executes dependency-ready steps.
4. Step execution applies retry/backoff and optional fallback logic on failure classes.
5. Sensitive actions require approval via `/api/v1/approvals` before progressing.
6. Run concludes as completed/failed/blocked/canceled, with timeline, metrics, and insight endpoints available for analysis.

## 8) Setup and Installation
### Prerequisites
- Python 3.11+
- Node.js 18+
- npm
- (Optional) Docker + Docker Compose

### Install dependencies
```bash
make setup
```

### Run backend
```bash
make dev-backend
```
API docs: `http://localhost:8000/docs`

### Run frontend
```bash
make dev-frontend
```

### Optional containerized stack
```bash
make up
```

### Run tests and lint
```bash
make test
make lint
```

### Run sample workflow demo
```bash
make run-orchestrator-demo
```

## 9) Example Use Cases
- Automating multi-step research/analysis tasks with explicit step routing and dependencies.
- Testing orchestrator resilience paths (timeouts, retries, fallback behavior).
- Demonstrating approval-gated workflow controls for sensitive actions.
- Inspecting workflow operations through timelines, run metrics, and reliability summaries.

## 10) Skills Demonstrated
- Multi-agent system design and orchestration architecture.
- Task decomposition, workflow routing, and dependency-aware execution.
- Tool abstraction via registry pattern and controlled tool invocation.
- API design for workflow lifecycle control and observability.
- Reliability engineering patterns: retries, fallback strategies, timeout handling.
- Human-in-the-loop workflow governance (approval gates).
- Full-stack implementation (Python APIs + TypeScript UI) for automation platforms.

## 11) Resume-Ready Project Description
Designed and built a **Multi-Agent Workflow Automation Platform** with **Python (FastAPI)** and **React/TypeScript** that orchestrates tasks across planner, worker, and reviewer agents. Implemented dependency-aware execution, tool-registry dispatch, retry/fallback controls, approval-gated actions, run replay, and operational telemetry (timeline, metrics, insights, audit). Delivered a modular orchestration architecture suitable for extension into production LLM workflows and enterprise automation pipelines.

## 12) Future Improvements
- Add optional live LLM planning/routing while preserving deterministic test mode.
- Expand tool adapters from simulated endpoints to real external services.
- Add richer authn/authz and multi-tenant policy controls.
- Enhance queueing/concurrency controls and background worker execution.
- Extend frontend with richer real-time run streaming and deeper graph analytics.
