import pytest
from src.parse_analyzed import get_player_ranks
from sgfmill import sgf


def test_correct_ranks():
    game1 = sgf.Sgf_game.from_string("(;FF[4]GM[1]SZ[9]CA[UTF-8]BR[4d]WR[3k];B[ee];W[ge])")
    assert (4, -2) == get_player_ranks(game1)
    game2 = sgf.Sgf_game.from_string("(;FF[4]GM[2]SZ[19]CA[UTF-16]BR[9d]WR[14k];B[dd];W[ge])")
    assert (9, -13) == get_player_ranks(game2)


def test_no_ranks():
    game1 = sgf.Sgf_game.from_string("(;FF[4]GM[1]SZ[9]CA[UTF-8];B[ee];W[ge])")
    assert (None, None) == get_player_ranks(game1)
    game2 = sgf.Sgf_game.from_string("(;GM[2]SZ[19]BR[5d];B[dd])")
    assert (5, None) == get_player_ranks(game2)


def test_incorrect_ranks():
    game = sgf.Sgf_game.from_string("(;FF[4]GM[1]SZ[9]CA[UTF-8]BR[4p]WR[9p];B[ee];W[ge]; B[de])")
    with pytest.raises(AttributeError, match="incorrect rank*"):
        get_player_ranks(game)