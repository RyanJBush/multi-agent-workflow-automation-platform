![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![CI](https://github.com/RyanJBush/Multi-agent-workflow-orchestration-platform/actions/workflows/ci.yml/badge.svg)

# Orion AI

> A multi-agent workflow orchestration platform that decomposes tasks into executable steps, routes them to specialized worker agents, enforces approval gates for sensitive operations, and provides full execution telemetry — built to explore the architecture of production agentic systems.

---

## 🎯 What I Built & Why

Single-agent LLM systems break down quickly on complex, multi-step tasks. I built Orion AI to explore what a production-grade agent orchestration layer actually requires:

- **Planner + worker agent separation** — a planner agent decomposes high-level tasks into typed steps, then routes each step to a worker agent that executes it via a registered tool. This mirrors the supervisor/worker pattern used in production agentic frameworks like LangGraph and AutoGen.
- **Tool registry + abstraction layer** — tools (`echo`, `math`, `flaky`, `slow_echo`, `sensitive_echo`) are registered with typed schemas, allowing agents to call them without knowing their implementation. The `flaky` and `slow_echo` tools intentionally model real failure modes (timeouts, retries).
- **Approval gates** — sensitive tool calls require human approval before execution, reflecting the human-in-the-loop requirements of real enterprise agentic deployments
- **Memory services** — both basic key-value and vector (FAISS) memory backends let agents persist and retrieve context across workflow steps
- **Execution telemetry** — every run produces a timestamped timeline, per-step metrics, and an insights summary — observable, debuggable agent behavior from day one

---

## 📷 Features

- **Task orchestration** — submit tasks, watch them decompose into typed steps and execute across worker agents
- **Tool registry** — pluggable tool abstraction with typed schemas and default built-in tools
- **Retry & fallback logic** — configurable retries per step with fallback actions on failure
- **Approval workflow** — sensitive tool calls require explicit human approval/rejection before execution
- **Memory services** — basic key-value + FAISS vector memory with persistence
- **Execution telemetry** — run timeline, per-step metrics, and AI-generated insights per run
- **Pause / resume / cancel / replay** — full run lifecycle controls
- **Usage quotas & audit logging** — workspace-scoped quotas and full audit trail
- **React workflow dashboard** — execution graph, timeline, per-step detail panel, and live telemetry
- **Docker Compose** — one-command local stack

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + SQLAlchemy + PostgreSQL |
| Agent Runtime | Custom orchestration engine (planner + worker pattern) |
| Memory | FAISS (vector) + key-value store |
| Frontend | React + Vite + TypeScript |
| Infra | Docker Compose + GitHub Actions CI |

---

## 🚀 Quick Start

### Prerequisites
- Docker + Docker Compose
- Python 3.11+
- Node.js 20+

### Docker (Recommended)
```bash
make up
# Backend API:  http://localhost:8000
# Frontend:     http://localhost:5173
# PostgreSQL:   localhost:5432
```

### Local Development
```bash
make setup
cp backend/.env.example backend/.env
make dev-backend    # Terminal 1
make dev-frontend   # Terminal 2
```

### Quality Checks
```bash
make test
make lint
```

---

## 🗂️ Repository Structure

```
backend/    FastAPI API, orchestration engine, tool registry, agent runtime, memory services, tests
frontend/   React workflow dashboard (execution graph, timeline, step detail, telemetry)
docs/       Architecture, API reference
```

---

## 📘 Demo Flow

1. Start services with `make up`
2. Seed demo workflow templates:
   ```bash
   make demo-seed
   ```
3. List templates and run one:
   ```bash
   curl http://localhost:8000/api/v1/workflows/templates
   curl -X POST http://localhost:8000/api/v1/workflows/templates/<id>/run
   ```
4. Inspect run timeline, metrics, and insights:
   ```bash
   curl http://localhost:8000/api/v1/workflows/runs/<run_id>/timeline
   curl http://localhost:8000/api/v1/workflows/runs/<run_id>/metrics
   curl http://localhost:8000/api/v1/workflows/runs/<run_id>/insights
   ```
5. Open the **Workflow Execution** page in the frontend to demonstrate pause/resume/cancel/replay with live telemetry

Demo workflows include: research, analysis, and multi-step reasoning templates.

Full API reference: `docs/api.md`

---

## 📝 Key Learnings

- Separating the planner and worker agents — rather than having one agent do everything — makes orchestration far more predictable and debuggable
- Human-in-the-loop approval gates are a hard requirement for any agent system that can take consequential actions; retrofitting them is painful
- Execution telemetry (timeline, per-step metrics, insights) is what turns an opaque agent run into something you can actually debug and improve

---

## 📄 License

MIT
