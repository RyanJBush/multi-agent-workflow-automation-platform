# Orion — Multi-Agent Workflow Orchestration Platform

Orion is a **portfolio-scale orchestrator demo** built by a **University of Maryland student studying Information Science and Electrical Engineering with a Business minor**. It demonstrates how a backend can coordinate specialized agents over a workflow graph while keeping execution traceable in both API responses and UI views.

## Project Positioning (Honest Behavior Statement)
Orion currently uses **stub-based agents and deterministic tools**. The planner, worker, and reviewer roles are implemented in code, but they do **not** call external LLM APIs in the default flow. This repository is focused on orchestration design patterns, reliability controls, and observability for a student portfolio demo.

## What Orion Demonstrates
- Multi-agent role separation (planner, worker, reviewer).
- Typed workflow decomposition into dependency-aware DAG steps.
- Retry + fallback controls for failed steps.
- Approval-gated sensitive actions that pause and resume runs.
- Audit logs and usage-style metrics for replay and walkthroughs.

## Agent Graph Overview
For full details, see [`docs/architecture.md`](docs/architecture.md).

High-level flow:
1. **Planner Agent** decomposes a user goal into ordered steps and dependencies.
2. **Execution Engine** starts dependency-ready steps.
3. **Worker Agent** executes each step via the tool registry.
4. **Reviewer Agent** records review decisions and can support approval-gated steps.
5. **Run Store + Audit** persist state transitions, events, and metrics.

Agent responsibilities:
- **Planner Agent**: produces deterministic plan structures from goal text.
- **Worker Agent**: dispatches named tool calls and records step outcomes.
- **Reviewer Agent**: captures review traces and approval outcomes.
- **Tools**: deterministic stubs (search/math/http/code/etc.) used to simulate orchestration behavior.

## Architecture
- Architecture guide: [`docs/architecture.md`](docs/architecture.md)
- API surface summary: [`docs/api.md`](docs/api.md)
- Codebase map: [`docs/codebase-overview.md`](docs/codebase-overview.md)

## How to Run Locally

### 1) Install dependencies
```bash
make setup
```

### 2) Start services
**Backend API**
```bash
make dev-backend
```

**Frontend UI (new terminal)**
```bash
make dev-frontend
```

Optional full stack via containers:
```bash
make up
```

### 3) Run a local orchestrator demo workflow
With backend running on `http://localhost:8000`:
```bash
make run-orchestrator-demo
```

## Demo Workflow Walkthrough
A typical demo sequence:
1. Open API docs at `http://localhost:8000/docs`.
2. Run `make run-orchestrator-demo` to submit a goal-driven workflow.
3. Inspect run state, step transitions, retries, and approval gating in API/UI.
4. Review screenshots in [`docs/screenshots/README.md`](docs/screenshots/README.md).
5. Open the design page at [`docs/preview/index.html`](docs/preview/index.html).

## Portfolio Preview + Screenshots
- Screenshot index: [`docs/screenshots/README.md`](docs/screenshots/README.md)
- Portfolio/UI preview: [`docs/preview/index.html`](docs/preview/index.html)

## Notes on LLM Integration
No API key is required for the default demo because the implementation is stub-based and deterministic.

If you later add an LLM-backed planner/router, store secrets in local environment variables (for example via `.env`) and **never commit API keys**.

## Resume Bullets
See [`docs/resume-bullets.md`](docs/resume-bullets.md).

## License
This project is licensed under [`LICENSE`](LICENSE).
