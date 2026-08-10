import pytest

from anti_cheat_detective.engine.stockfish import MoveEvaluation
from anti_cheat_detective.features.baseline import compute_player_baseline


def evaluation(ply: int, color: str, loss: int, match: bool) -> MoveEvaluation:
    return MoveEvaluation(
        ply=ply,
        color=color,
        played_move="e2e4" if match else "d2d4",
        best_move="e2e4",
        played_score_cp=20 - loss,
        best_score_cp=20,
        centipawn_loss=loss,
    )


def test_computes_white_baseline_only() -> None:
    rows = [
        evaluation(1, "white", 10, True),
        evaluation(2, "black", 80, False),
        evaluation(3, "white", 30, False),
    ]

    result = compute_player_baseline(rows, "white")

    assert result.move_count == 2
    assert result.acpl == 20
    assert result.median_centipawn_loss == 20
    assert result.top1_match_rate == 0.5


def test_rejects_missing_color() -> None:
    with pytest.raises(ValueError, match="No black"):
        compute_player_baseline([evaluation(1, "white", 0, True)], "black")

