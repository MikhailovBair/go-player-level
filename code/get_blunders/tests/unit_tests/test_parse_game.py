from src.parse_analyzed import parse_game


def check_game(path):
    results = parse_game(path, "./ranks_table.csv")
    assert len(results) == 4
    assert type(results["blunders_black"]) == list
    assert type(results["blunders_white"]) == list
    assert type(results["mistakes_black"]) == list
    assert type(results["mistakes_white"]) == list


def test_games():
    check_game("./tests/test_games/A.sgf")
    check_game("./tests/test_games/B.sgf")
