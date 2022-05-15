from sgfmill import sgf
from src.parse_analyzed import get_turns_list


def check_game(path):
    with open(path, "rb") as f:
        game = sgf.Sgf_game.from_bytes(f.read())

    turns_black, turns_white = get_turns_list(game)

    for turn in turns_black:
        assert turn.turn_number % 2 == 1
        assert turn.turn_number > 0

    for turn in turns_white:
        assert turn.turn_number % 2 == 0
        assert turn.turn_number > 0


def test_game_with_correct_ending():
    check_game("./tests/test_games/A-analyzed.sgf")


def test_game_with_incorrect_ending():
    check_game("./tests/test_games/B-analyzed.sgf")
