# Sample Data

`sample_tasks.json` contains five demo workflows that exercise the major
behaviors of the orchestration engine:

| Scenario | What it exercises |
|---|---|
| `research_automation` | Planner decomposition, search → compare → summarize routing |
| `ticket_triage` | HTTP-style tool calls, multi-step dependency chain |
| `business_report` | Math + summarization tools, approval-gated branches |
| `retry_and_fallback` | Retry policy + fallback action when a flaky tool fails |
| `human_in_the_loop` | Approval gate blocks the run until a reviewer decides |

Use `scripts/run_sample_workflow.py` to run any of these end-to-end against
an ephemeral SQLite database.
