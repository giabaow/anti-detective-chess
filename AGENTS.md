# Anti-cheat Detective — Project Context

## Goal

Build an explainable proof of concept for statistical detection of chess engine
assistance, inspired by Kenneth Regan's methods and extended with feature
engineering. Statistical signals are not proof of cheating.

## Non-negotiable constraints

- The report-writing LLM receives validated structured input only, never raw data.
- Every number produced by the agent must be checked against computed source data.
- Do not use Niemann as a positive validation case; use it only to examine false positives.
- Precision/recall cases require evidence independent of statistics.
- Always report sample size and limitations; do not overstate small-sample metrics.
- Cite Regan-derived formulas and distinguish them from original extensions.

## Status

- [x] Stage 0 — Initial repository and research constraints
- [x] Stage 1a — PGN parser, UCI wrapper, ACPL/T1 baseline
- [x] Stage 1 UI — PGN upload/paste, automatic polling, result display
- [ ] Stage 1b — Curated baseline data and reproducible download scripts
- [ ] Stage 2 — Advanced feature engineering
- [ ] Stage 3 — Structured report-writing agent
- [ ] Stage 4 — Evaluation and validation
- [ ] Stage 5 — Demo hardening and final report

**Next task:** add a small licensed/redistributable baseline dataset manifest,
source documentation, and an analysis CLI that writes reproducible JSON.

## Technical decisions

| Date | Decision | Reason |
|---|---|---|
| 2026-07-19 | Use a `src/` package and `uv` | Reproducible packaging and fast local setup |
| 2026-07-19 | Run two engine searches per move | Score the actual move against the unconstrained best move explicitly |
| 2026-07-19 | Keep in-memory FastAPI jobs for milestone 1 | Avoid premature Celery/Redis/DB complexity |
| 2026-07-19 | No accusation/classification endpoint yet | Baseline features are insufficient for a defensible conclusion |
| 2026-07-19 | Serve a dependency-free local web interface | Make the MVP usable without Swagger or a frontend build chain |

## Coding conventions

- English docstrings; Vietnamese comments are acceptable for complex reasoning.
- Every feature function requires unit tests before use in a model.
- Do not commit large PGN or baseline dumps. Provide a reproducible download script.
