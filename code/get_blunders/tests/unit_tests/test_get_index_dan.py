import pytest
from src.parse_analyzed import get_index_dan


def test_correct_rank():
    assert 1 == get_index_dan("2k")
    assert 2 == get_index_dan("14k")
    assert 1 == get_index_dan("9d")


def test_incorrect_rank():
    with pytest.raises(AttributeError, match="incorrect rank*"):
        get_index_dan("5")

    with pytest.raises(AttributeError, match="incorrect rank*"):
        get_index_dan("9p")

    with pytest.raises(AttributeError, match="incorrect rank*"):
        get_index_dan("9кю")