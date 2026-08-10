"""Stockfish UCI wrapper with explicit, reproducible scoring semantics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chess
import chess.engine
import chess.pgn


@dataclass(frozen=True, slots=True)
class AnalysisConfig:
    """Engine settings that materially affect all reported measurements."""

    depth: int = 18
    mate_score: int = 100_000

    def __post_init__(self) -> None:
        if self.depth < 1:
            raise ValueError("depth must be positive")
        if self.mate_score < 1:
            raise ValueError("mate_score must be positive")


@dataclass(frozen=True, slots=True)
class MoveEvaluation:
    """Engine measurements for one played half-move, from the mover's POV."""

    ply: int
    color: str
    played_move: str
    best_move: str
    played_score_cp: int
    best_score_cp: int
    centipawn_loss: int

    @property
    def top1_match(self) -> bool:
        """Return whether the player chose the engine's first move."""
        return self.played_move == self.best_move


def _score_cp(info: dict[str, Any], color: chess.Color, mate_score: int) -> int:
    score = info.get("score")
    if score is None:
        raise RuntimeError("Engine response did not include a score")
    value = score.pov(color).score(mate_score=mate_score)
    if value is None:
        raise RuntimeError("Engine score could not be converted to centipawns")
    return value


class StockfishAnalyzer:
    """Manage a Stockfish process and analyze games one move at a time."""

    def __init__(self, engine_path: str | Path, config: AnalysisConfig | None = None) -> None:
        self.engine_path = str(engine_path)
        self.config = config or AnalysisConfig()
        self._engine: chess.engine.SimpleEngine | None = None

    def __enter__(self) -> StockfishAnalyzer:
        self._engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        """Stop the UCI process if it is running."""
        if self._engine is not None:
            self._engine.quit()
            self._engine = None

    def analyze_game(self, game: chess.pgn.Game) -> list[MoveEvaluation]:
        """Compare every played move with the engine's best move.

        Each position is searched twice at the same depth: once without a root
        restriction and once restricted to the move actually played.
        """
        if self._engine is None:
            raise RuntimeError("Use StockfishAnalyzer as a context manager")

        board = game.board()
        evaluations: list[MoveEvaluation] = []
        limit = chess.engine.Limit(depth=self.config.depth)

        for ply, move in enumerate(game.mainline_moves(), start=1):
            mover = board.turn
            if move not in board.legal_moves:
                raise ValueError(f"Illegal move at ply {ply}: {move.uci()}")

            best_info = self._engine.analyse(board, limit)
            best_pv = best_info.get("pv", [])
            if not best_pv:
                raise RuntimeError(f"Engine response had no principal variation at ply {ply}")
            best_move = best_pv[0]
            played_info = self._engine.analyse(board, limit, root_moves=[move])

            best_score = _score_cp(best_info, mover, self.config.mate_score)
            played_score = _score_cp(played_info, mover, self.config.mate_score)
            evaluations.append(
                MoveEvaluation(
                    ply=ply,
                    color="white" if mover == chess.WHITE else "black",
                    played_move=move.uci(),
                    best_move=best_move.uci(),
                    played_score_cp=played_score,
                    best_score_cp=best_score,
                    centipawn_loss=max(0, best_score - played_score),
                )
            )
            board.push(move)

        return evaluations

