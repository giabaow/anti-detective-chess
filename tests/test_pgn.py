import pytest

from anti_cheat_detective.engine.pgn import PgnError, parse_pgn


def test_parse_valid_game() -> None:
    game = parse_pgn('[Event "Example"]\n\n1. e4 e5 2. Nf3 Nc6 1/2-1/2')

    assert len(list(game.mainline_moves())) == 4


@pytest.mark.parametrize("pgn", ["", "   ", '[Event "Empty"]\n\n*'])
def test_rejects_empty_game(pgn: str) -> None:
    with pytest.raises(PgnError):
        parse_pgn(pgn)


def test_rejects_multiple_games() -> None:
    pgn = '[Event "One"]\n\n1. e4 e5 *\n\n[Event "Two"]\n\n1. d4 d5 *'

    with pytest.raises(PgnError, match="one game"):
        parse_pgn(pgn)

