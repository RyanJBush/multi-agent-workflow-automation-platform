# Screenshots

This folder holds the portfolio captures referenced from the top-level
[`README.md`](../../README.md). All seven captures below are real PNGs
taken from a local run with the demo seed data loaded.

> The CLI demo (`python scripts/run_sample_workflow.py`) produces the
> same evidence in text form if you want to reproduce the run state
> these images were captured against.

---

## Captures (in order of recruiter impact)

| Filename | What it shows | Where in the app | Status |
|---|---|---|---|
| `workflow-builder.png` | Tasks page with submit form and recent task list across all seeded scenarios | `TasksPage.tsx` | ✅ captured |
| `dag-view.png` | DAG with dependency edges between planned steps, plus run insight panel | `components/workflow/WorkflowGraph.tsx` on `WorkflowExecutionPage` (run #1) | ✅ captured |
| `run-logs.png` | Per-step execution log with selected step detail, retries, and reviewer events | `components/workflow/ExecutionLogPanel.tsx` (run #6, retry/fallback scenario) | ✅ captured |
| `dashboard-metrics.png` | KPI cards: total runs, running, completed, avg step latency, completion rate | `DashboardPage.tsx` | ✅ captured |
| `approval-queue.png` | The `sensitive_echo` step in `blocked` state awaiting a human approval decision | `WorkflowExecutionPage` after running the human-in-the-loop scenario (run #7) | ✅ captured |
| `agent-monitor.png` | Planner / worker / reviewer status table plus tool health table | `AgentMonitorPage.tsx` | ✅ captured |
| `api-docs.png` | FastAPI auto-generated `/docs` (OpenAPI) page showing all tagged routes | `http://localhost:8000/docs` | ✅ captured |

> **Cost tracker note.** Token / dollar cost tracking is **not** implemented
> (tools are deterministic stubs, not LLM calls). If you want a
> "cost-style" screenshot, capture the **run metrics** view instead —
> retries, fallbacks, and latency are the cost signals Orion actually
> measures today. Document this clearly in any portfolio caption.

---

## How to capture / re-capture

```bash
# 1. Bring up the full stack
docker compose up --build

# 2. In another shell, seed templates and run scenarios so there's data to display
curl -X POST http://localhost:8000/api/v1/workflows/templates/seed-demo
curl -X POST http://localhost:8000/api/v1/agents/seed-demo
for tid in 1 2 3 4 6 7 5; do
  curl -X POST http://localhost:8000/api/v1/workflows/templates/${tid}/run
done
# Open an approval for the sensitive-export run (run id 7) so the queue is populated:
curl -X POST http://localhost:8000/api/v1/approvals \
  -H "Content-Type: application/json" \
  -d '{"run_id": 7, "step_id": "step-1", "tool_name": "sensitive_echo", "reason": "Sensitive export requires explicit human approval"}'

# 3. Open http://localhost:5173 and capture each route above
# 4. Open http://localhost:8000/docs and capture the OpenAPI page
```

The captures committed here were produced with Playwright at a
1440×900 viewport, 2× device scale factor, and re-encoded to a 256-colour
palette so each PNG stays under 500 KB without losing legibility.

Suggested capture settings:

- 1440×900 viewport for desktop screenshots, 2–4× for retina output.
- Hide browser chrome / scrollbars; use Chrome DevTools "Capture full
  size screenshot", Playwright `page.screenshot(full_page=True)`,
  or `Cmd+Shift+4` (macOS) / `Win+Shift+S` (Windows).
- Save as PNG, keep under 500 KB per image. `oxipng`, `pngquant`, or
  a quick Pillow palette quantize all work.

---

## Naming convention

- All lowercase, hyphen-separated, `.png`.
- Match the filenames in the table above so README image links keep working.

---

## Capture environment notes

The committed PNGs were taken against a local stack started outside
Docker (no docker daemon was available in the capture environment).
The backend was launched directly with
`uvicorn app.main:app --host 0.0.0.0 --port 8000` and the frontend with
`VITE_API_BASE_URL=http://localhost:8000/api/v1 npm run dev`. To let
the dev-server frontend talk to the backend across origins, permissive
CORS was enabled on the FastAPI app at capture time — this is **not**
checked in, the production `app/main.py` is untouched.
