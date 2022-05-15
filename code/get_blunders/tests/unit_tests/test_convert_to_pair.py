from src.parse_analyzed import convert_to_pair


def test_convertation():
    assert 1, 9 == convert_to_pair("A9")
    assert 7, 8 == convert_to_pair("G8")
