# Screenshots

Placeholders for portfolio screenshots. Replace these with real captures from
the running app once you have a recording set up.

Suggested captures:

1. `dashboard.png` — `/` route, KPI cards + recent runs.
2. `workflow-graph.png` — `WorkflowGraph` panel mid-run with one step highlighted.
3. `execution-log.png` — `ExecutionLogPanel` showing per-agent reasoning traces and retries.
4. `approval-queue.png` — a sensitive step in `blocked` state waiting on a reviewer decision.
5. `agent-monitor.png` — `AgentMonitorPage` listing planner/worker/reviewer with last status.

To capture:

```bash
docker compose up --build
# open http://localhost:5173 and run a sample task from data/sample_tasks.json
```
