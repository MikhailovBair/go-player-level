from sgfmill import sgf
from src.parse_analyzed import get_worst_errors


def check_game(path: str):
    with open(path, "rb") as f:
        game = sgf.Sgf_game.from_bytes(f.read())
    worst_turns = get_worst_errors(game, "../ranks_table.csv")
    assert 4 == len(worst_turns)
    assert type(worst_turns['blunders_black']) == list
    assert type(worst_turns['blunders_white']) == list
    assert type(worst_turns['mistakes_black']) == list
    assert type(worst_turns['mistakes_white']) == list


def test_games():
    check_game("test_games/A-analyzed.sgf")
    check_game("test_games/B-analyzed.sgf")
