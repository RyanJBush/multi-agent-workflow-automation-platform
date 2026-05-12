"""Run a sample multi-agent workflow end-to-end from the CLI.

Usage:
    python scripts/run_sample_workflow.py
    python scripts/run_sample_workflow.py --goal "Research three vendors and summarize"

Boots an in-process FastAPI test client against an in-memory SQLite DB,
submits a task, polls until completion, and prints the run timeline.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections.abc import Generator
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

os.environ.setdefault("ORION_JWT_SECRET", "demo-secret-key")

from app.db.base import Base  # noqa: E402
from app.db.session import get_db  # noqa: E402
from app.main import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import Session, sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402


def _setup_in_memory_db() -> Session:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=Session)
    return factory()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a sample Orion workflow.")
    parser.add_argument(
        "--goal",
        default="Search the vendor landscape. Then compare three options. Summarize findings.",
        help="High-level goal for the planner agent.",
    )
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()

    db = _setup_in_memory_db()

    def _override_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = _override_db

    with TestClient(app) as client:
        print(f"[orion-demo] submitting goal: {args.goal!r}")
        resp = client.post(
            "/api/v1/tasks/submit",
            json={"title": args.goal, "description": args.goal},
        )
        resp.raise_for_status()
        payload = resp.json()
        run_id = payload.get("id")
        print(f"[orion-demo] run_id={run_id} initial_status={payload.get('status')!r}")

        deadline = time.time() + args.timeout
        status = "unknown"
        while time.time() < deadline:
            run = client.get(f"/api/v1/workflows/runs/{run_id}").json()
            status = run.get("status")
            print(f"[orion-demo] run status: {status}")
            if status in {"completed", "failed", "cancelled", "blocked"}:
                break
            time.sleep(0.5)

        timeline = client.get(f"/api/v1/workflows/runs/{run_id}/timeline").json()
        print("[orion-demo] timeline (truncated):")
        print(json.dumps(timeline, indent=2, default=str)[:4000])
        print(f"[orion-demo] final status: {status}")
    app.dependency_overrides.clear()
    return 0 if status == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
