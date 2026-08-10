"""Schemas that prevent a report agent from receiving raw game data."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PlayerEvidence(BaseModel):
    """Validated numeric evidence available to a narrative agent."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    color: Literal["white", "black"]
    move_count: int = Field(ge=1)
    acpl: float = Field(ge=0)
    median_centipawn_loss: float = Field(ge=0)
    top1_match_rate: float = Field(ge=0, le=1)


class GameAnalysisEvidence(BaseModel):
    """Complete structured input permitted at the future LLM boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    engine_name: str = Field(min_length=1)
    engine_depth: int = Field(ge=1)
    white: PlayerEvidence
    black: PlayerEvidence
    limitations: tuple[str, ...] = (
        "Statistical engine agreement is not proof of cheating.",
        "Single-game measurements are highly uncertain.",
    )

