"""Strict helpers for parsing PGN input."""

from __future__ import annotations

from io import StringIO

import chess.pgn


class PgnError(ValueError):
    """Raised when PGN input cannot be parsed into a usable game."""


def parse_pgn(pgn_text: str) -> chess.pgn.Game:
    """Parse exactly one non-empty chess game from a PGN string.

    A trailing second game is rejected so that an API job cannot silently
    analyze less data than the caller submitted.
    """
    if not pgn_text.strip():
        raise PgnError("PGN input is empty")

    stream = StringIO(pgn_text)
    game = chess.pgn.read_game(stream)
    if game is None:
        raise PgnError("No chess game found in PGN input")
    if game.errors:
        raise PgnError(f"Invalid PGN: {game.errors[0]}")
    if not list(game.mainline_moves()):
        raise PgnError("PGN game has no moves")

    second_game = chess.pgn.read_game(stream)
    if second_game is not None:
        raise PgnError("Submit one game per analysis job")
    return game

