"""Minimal asynchronous-job API for one-game Stockfish analysis."""

from __future__ import annotations

import os
from dataclasses import asdict
from enum import StrEnum
from pathlib import Path
from threading import Lock
from uuid import UUID, uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict, Field

from anti_cheat_detective.agent.schemas import GameAnalysisEvidence, PlayerEvidence
from anti_cheat_detective.engine.pgn import PgnError, parse_pgn
from anti_cheat_detective.engine.stockfish import AnalysisConfig, StockfishAnalyzer
from anti_cheat_detective.features.baseline import compute_player_baseline

app = FastAPI(title="Anti-cheat Detective", version="0.1.0")
_index_path = Path(__file__).parent.parent / "web" / "index.html"


class JobStatus(StrEnum):
    """Analysis job lifecycle."""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisRequest(BaseModel):
    """One PGN game submitted for analysis."""

    model_config = ConfigDict(extra="forbid")
    pgn: str = Field(min_length=1, max_length=250_000)


class AnalysisJob(BaseModel):
    """Public job representation."""

    job_id: UUID
    status: JobStatus
    result: GameAnalysisEvidence | None = None
    error: str | None = None


_jobs: dict[UUID, AnalysisJob] = {}
_jobs_lock = Lock()


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index() -> HTMLResponse:
    """Serve the local single-page analysis interface."""
    return HTMLResponse(_index_path.read_text(encoding="utf-8"))


def _set_job(job: AnalysisJob) -> None:
    with _jobs_lock:
        _jobs[job.job_id] = job


def _run_analysis(job_id: UUID, pgn: str) -> None:
    _set_job(AnalysisJob(job_id=job_id, status=JobStatus.RUNNING))
    try:
        game = parse_pgn(pgn)
        depth = int(os.getenv("STOCKFISH_DEPTH", "18"))
        engine_path = os.getenv("STOCKFISH_PATH", "stockfish")
        config = AnalysisConfig(depth=depth)
        with StockfishAnalyzer(engine_path, config) as analyzer:
            evaluations = analyzer.analyze_game(game)

        white = compute_player_baseline(evaluations, "white")
        black = compute_player_baseline(evaluations, "black")
        result = GameAnalysisEvidence(
            engine_name="Stockfish",
            engine_depth=depth,
            white=PlayerEvidence(**asdict(white)),
            black=PlayerEvidence(**asdict(black)),
        )
        _set_job(AnalysisJob(job_id=job_id, status=JobStatus.COMPLETED, result=result))
    except (OSError, ValueError, RuntimeError, PgnError) as exc:
        _set_job(AnalysisJob(job_id=job_id, status=JobStatus.FAILED, error=str(exc)))


@app.get("/health")
def health() -> dict[str, str]:
    """Return process health without launching the chess engine."""
    return {"status": "ok"}


@app.post("/v1/analyses", response_model=AnalysisJob, status_code=status.HTTP_202_ACCEPTED)
def create_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks) -> AnalysisJob:
    """Validate PGN immediately and enqueue engine analysis."""
    try:
        parse_pgn(request.pgn)
    except PgnError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    job = AnalysisJob(job_id=uuid4(), status=JobStatus.QUEUED)
    _set_job(job)
    background_tasks.add_task(_run_analysis, job.job_id, request.pgn)
    return job


@app.get("/v1/analyses/{job_id}", response_model=AnalysisJob)
def get_analysis(job_id: UUID) -> AnalysisJob:
    """Fetch the latest state of an analysis job."""
    with _jobs_lock:
        job = _jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found")
    return job
