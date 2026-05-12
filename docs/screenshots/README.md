# Screenshots

This folder holds the portfolio captures referenced from the top-level
[`README.md`](../../README.md). The files below are placeholders today —
replace each with a real PNG from a local run before sharing the repo
externally with a recruiter.

> Until real captures land, the README and demo-runbook are the
> recruiter-facing surface. The CLI demo
> (`python scripts/run_sample_workflow.py`) produces the same evidence in
> text form.

---

## Required captures (in order of recruiter impact)

| Filename | What it shows | Where in the app |
|---|---|---|
| `workflow-builder.png` | The workflow builder / construction surface | `TasksPage.tsx` or the `WorkflowExecutionPage` create flow |
| `dag-view.png` | DAG with dependency edges between planned steps | `components/workflow/WorkflowGraph.tsx` on `WorkflowExecutionPage` |
| `run-logs.png` | Per-step execution log with retries and reasoning traces | `components/workflow/ExecutionLogPanel.tsx` |
| `dashboard-metrics.png` | KPI cards: completion rate, retry rate, avg latency | `DashboardPage.tsx` |
| `approval-queue.png` | A sensitive step in `blocked` state awaiting approval | `WorkflowExecutionPage` after running the human-in-the-loop scenario |
| `agent-monitor.png` | Planner / worker / reviewer status table | `AgentMonitorPage.tsx` |
| `api-docs.png` | FastAPI auto-generated `/docs` (OpenAPI) page | `http://localhost:8000/docs` |

> **Cost tracker note.** Token / dollar cost tracking is **not** implemented
> (tools are deterministic stubs, not LLM calls). If you want a
> "cost-style" screenshot, capture the **run metrics** view instead —
> retries, fallbacks, and latency are the cost signals Orion actually
> measures today. Document this clearly in any portfolio caption.

---

## How to capture

```bash
# 1. Bring up the full stack
docker compose up --build

# 2. In another shell, run a scenario so there's data to display
python scripts/run_sample_workflow.py
python scripts/run_sample_workflow.py \
  --goal "Export the sensitive customer extract. This step requires explicit human approval."

# 3. Open http://localhost:5173 and capture each route above
# 4. Open http://localhost:8000/docs and capture the OpenAPI page
```

Suggested capture settings:

- 1440×900 viewport for desktop screenshots, 4× for retina output.
- Hide browser chrome / scrollbars; use Chrome DevTools "Capture full
  size screenshot" or `Cmd+Shift+4` (macOS) / `Win+Shift+S` (Windows).
- Save as PNG, keep under 500 KB per image (use `oxipng` or `pngquant`
  if needed).

---

## Naming convention

- All lowercase, hyphen-separated, `.png`.
- Match the filenames in the table above so README image links keep working.
