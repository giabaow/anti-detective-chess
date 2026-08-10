from typing import Any

import chess
import chess.engine
import pytest

from anti_cheat_detective.engine.pgn import parse_pgn
from anti_cheat_detective.engine.stockfish import AnalysisConfig, StockfishAnalyzer


class FakeEngine:
    def __init__(self) -> None:
        self.quit_called = False

    def analyse(
        self,
        board: chess.Board,
        _limit: chess.engine.Limit,
        root_moves: list[chess.Move] | None = None,
    ) -> dict[str, Any]:
        best_move = chess.Move.from_uci("e2e4")
        score = 20 if root_moves else 50
        return {
            "pv": root_moves or [best_move],
            "score": chess.engine.PovScore(chess.engine.Cp(score), board.turn),
        }

    def quit(self) -> None:
        self.quit_called = True


def test_analyzes_played_move_against_best_move(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = FakeEngine()
    monkeypatch.setattr(chess.engine.SimpleEngine, "popen_uci", lambda _path: engine)
    game = parse_pgn('[Event "One ply"]\n\n1. d4 *')

    with StockfishAnalyzer("fake-stockfish", AnalysisConfig(depth=12)) as analyzer:
        result = analyzer.analyze_game(game)

    assert len(result) == 1
    assert result[0].played_move == "d2d4"
    assert result[0].best_move == "e2e4"
    assert result[0].centipawn_loss == 30
    assert result[0].top1_match is False
    assert engine.quit_called is True


@pytest.mark.parametrize("kwargs", [{"depth": 0}, {"mate_score": 0}])
def test_rejects_invalid_engine_config(kwargs: dict[str, int]) -> None:
    with pytest.raises(ValueError):
        AnalysisConfig(**kwargs)


def test_requires_context_manager() -> None:
    game = parse_pgn('[Event "One ply"]\n\n1. e4 *')

    with pytest.raises(RuntimeError, match="context manager"):
        StockfishAnalyzer("fake-stockfish").analyze_game(game)
