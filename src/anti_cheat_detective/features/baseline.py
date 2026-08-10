"""Transparent baseline features derived from per-move engine evaluations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from statistics import fmean, median
from typing import Literal

from anti_cheat_detective.engine.stockfish import MoveEvaluation


@dataclass(frozen=True, slots=True)
class PlayerBaseline:
    """Simple aggregate metrics for one side in one game."""

    color: Literal["white", "black"]
    move_count: int
    acpl: float
    median_centipawn_loss: float
    top1_match_rate: float


def compute_player_baseline(
    evaluations: Iterable[MoveEvaluation], color: Literal["white", "black"]
) -> PlayerBaseline:
    """Compute ACPL and top-1 agreement for one player.

    This function intentionally performs no classification and assigns no
    cheating probability.
    """
    selected = [item for item in evaluations if item.color == color]
    if not selected:
        raise ValueError(f"No {color} move evaluations were supplied")

    losses = [item.centipawn_loss for item in selected]
    return PlayerBaseline(
        color=color,
        move_count=len(selected),
        acpl=fmean(losses),
        median_centipawn_loss=float(median(losses)),
        top1_match_rate=fmean(item.top1_match for item in selected),
    )
