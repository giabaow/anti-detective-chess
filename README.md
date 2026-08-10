# Anti-cheat Detective

An explainable research prototype for detecting statistical signals consistent
with chess engine assistance. A high engine agreement score is **not proof of
cheating**; every output must be interpreted with context and independent
evidence.

## Current scope

- Parse PGN safely with `python-chess`.
- Evaluate each played move and the engine's preferred move with Stockfish.
- Calculate average centipawn loss (ACPL) and top-1 move agreement.
- Submit analysis through a small FastAPI background job API.
- Keep the future report-writing agent behind validated Pydantic schemas.

This first milestone does not train a classifier and does not make cheating
accusations.

## Local setup

Requirements: Python 3.11+, `uv`, and a Stockfish binary.

```bash
uv sync --extra dev
export STOCKFISH_PATH=/path/to/stockfish
uv run uvicorn anti_cheat_detective.api.app:app --reload
```

Open `http://127.0.0.1:8000` for the analysis interface. The developer API
documentation remains available at `http://127.0.0.1:8000/docs`. Run checks with:

```bash
uv run pytest
uv run ruff check .
```

## Docker

```bash
docker compose up --build
```

## API example

```bash
curl -X POST http://127.0.0.1:8000/v1/analyses \
  -H 'content-type: application/json' \
  -d '{"pgn":"[Event \"Example\"]\\n\\n1. e4 e5 2. Nf3 Nc6 1/2-1/2"}'
```

The response contains a job ID. Poll `GET /v1/analyses/{job_id}` until its
status is `completed` or `failed`.

## Web interface

The home page accepts either a `.pgn` file or pasted PGN text, submits the game,
polls the background job automatically, and displays per-player ACPL and top-1
move agreement. It deliberately avoids producing an accusation or cheating
probability from a single game.

## Interpretation constraints

- ACPL varies with rating, position complexity, time control, game phase, and
  engine settings.
- Small confirmed-cheating datasets cannot support trustworthy headline
  precision/recall claims.
- The Niemann case is reserved for false-positive behavior testing, not a
  positive validation example.
- Positive evaluation cases require evidence independent of statistical move
  matching. Sources for both PGNs and external evidence must be recorded.
- Regan-derived formulas must be cited and separated from project-specific
  extensions in the final report.

## Repository layout

`src/anti_cheat_detective/engine` contains PGN and UCI integration;
`features` contains tested deterministic features; `agent` contains the strict
structured boundary for future narrative generation; and `api` exposes the
MVP. Large or downloaded PGN files remain ignored by Git.
