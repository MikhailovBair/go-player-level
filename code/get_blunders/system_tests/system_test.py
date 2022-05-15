import requests


def test_correct():
    """
    Test with correct sgf file
    Getting json with blunders and mistakes
    """
    answer = dict(requests.post("http://localhost:5000", files={"file": open("../tests/test_games/B.sgf", 'rb')}).json())
    assert len(answer) == 4
    assert type(answer["blunders_black"]) == list
    assert type(answer["blunders_white"]) == list
    assert type(answer["mistakes_black"]) == list
    assert type(answer["mistakes_white"]) == list
    for turn in answer["blunders_black"]:
        assert type(turn) == int
        assert turn >= 1
    print(answer)


def test_incorrect_file():
    """
        Test with incorrect correct sgf file
        Getting json containing error
    """
    answer = dict(requests.post("http://localhost:5000", files={"file": open("../tests/test_games/C.sgf", 'rb')}).json())
    assert len(answer) == 1
    print(answer["error"])


test_correct()
test_incorrect_file()
