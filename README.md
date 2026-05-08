![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![CI](https://github.com/RyanJBush/Multi-agent-workflow-orchestration-platform/actions/workflows/ci.yml/badge.svg)

# Orchestrix

> A production-style multi-agent workflow orchestration platform where specialized AI agents are composed into task pipelines, each with defined roles, tool access, retry logic, and cost tracking — built to reflect how real LLM-powered automation systems are structured.

---

## 🎯 What I Built & Why

Single-agent LLM systems break down on complex tasks. I built Orchestrix to practice the core patterns of multi-agent orchestration: how you decompose work, route between agents, handle failures gracefully, and keep costs observable.

- **Role-specialized agents** — each agent has a defined capability contract (planner, researcher, writer, validator, critic) with scoped tool access, preventing agents from overreaching their role
- **Directed task graph execution** — workflows are defined as DAGs; the orchestrator resolves dependencies and executes agents in topological order with parallel branches where possible
- **Retry + fallback logic** — per-agent retry policies with exponential backoff, fallback agent routing, and graceful degradation so one tool failure doesn’t cascade
- **Token cost tracking** — every agent invocation logs prompt + completion tokens; `GET /api/workflows/{id}/cost` returns a per-agent, per-run cost breakdown

---

## 🏗️ Architecture

```mermaid
flowchart TD
    subgraph Client["Client Layer"]
        UI["React + TypeScript\nWorkflow Builder + Run Monitor"]
    end

    subgraph API["FastAPI Backend"]
        R_WORKFLOWS["workflows router\n/api/workflows"]
        R_AGENTS["agents router\n/api/agents"]
        R_RUNS["runs router\n/api/runs"]
        R_TASKS["tasks router\n/api/tasks"]
        R_TOOLS["tools router\n/api/tools"]
        R_COST["cost router\n/api/cost"]
        R_AUTH["auth router"]
    end

    subgraph Orchestration["Orchestration Engine"]
        PLANNER_AGENT["Planner\nAgent"]
        RESEARCHER_AGENT["Researcher\nAgent"]
        WRITER_AGENT["Writer\nAgent"]
        VALIDATOR_AGENT["Validator\nAgent"]
        CRITIC_AGENT["Critic\nAgent"]
        SCHEDULER["DAG Scheduler\n(topological exec)"]
        RETRY["Retry + Fallback\nController"]
        COST_TRACKER["Token Cost\nTracker"]
    end

    subgraph Tools["Agent Tools"]
        WEB["Web Search"]
        CODE["Code Executor"]
        FILE["File Reader"]
        LLMCALL["LLM Call"]
    end

    subgraph Data["Data Layer"]
        PG[("PostgreSQL\nWorkflows · Runs · Tasks · Costs")]
    end

    UI -->|"JWT"| R_AUTH
    UI --> R_WORKFLOWS & R_RUNS & R_COST
    R_WORKFLOWS --> SCHEDULER
    SCHEDULER --> PLANNER_AGENT & RESEARCHER_AGENT & WRITER_AGENT & VALIDATOR_AGENT & CRITIC_AGENT
    PLANNER_AGENT & RESEARCHER_AGENT & WRITER_AGENT --> Tools
    Tools --> RETRY
    SCHEDULER --> COST_TRACKER
    R_WORKFLOWS & R_RUNS & R_TASKS --> PG
```

---

## 📷 Features

- **Role-specialized agents** — Planner, Researcher, Writer, Validator, Critic with scoped tool access
- **DAG workflow execution** — dependency-resolved topological scheduling with parallel branches
- **Retry + fallback logic** — per-agent exponential backoff and graceful degradation
- **Token cost tracking** — per-agent, per-run cost breakdown with budget alerts
- **Workflow builder UI** — visual agent graph construction and real-time run monitoring
- **Run history & replay** — full execution traces with per-step logs and outputs
- **Docker Compose** — one-command local stack

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + SQLAlchemy + PostgreSQL |
| Agent Orchestration | Custom DAG executor + LLM tool calling |
| Frontend | React + Vite + TypeScript |
| Infra | Docker Compose + GitHub Actions CI |

---

## 🚀 Quick Start

```bash
docker compose up --build
# Backend API docs: http://localhost:8000/docs
# Frontend:         http://localhost:5173
```

### Local Development
```bash
cd backend && pip install -e .[dev]
cp .env.example .env   # add your LLM API key
uvicorn app.main:app --reload

cd frontend && npm ci && npm run dev
```

### Quality Checks
```bash
make lint && make test
```

---

## 🗂️ Repository Structure

```
backend/    FastAPI API, DAG orchestrator, agent roles, tool registry, cost tracker, tests
frontend/   React workflow builder and run monitor
docs/       Architecture, agent design, workflow examples
```

---

## 📝 Key Learnings

- Role specialization is the most important architectural decision in multi-agent systems — general-purpose agents drift; scoped agents stay predictable
- Cost tracking is a first-class production concern, not an afterthought; token costs compound quickly across nested agent calls
- Retry + fallback logic at the agent level (not just the API level) is what separates a demo from a reliable system

---

## 📄 License

MIT
