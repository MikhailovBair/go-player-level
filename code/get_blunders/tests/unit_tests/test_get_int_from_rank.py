import pytest
from src.parse_analyzed import get_int_from_rank


def test_ku_ranks():
    assert -14 == get_int_from_rank("15k")
    assert 0 == get_int_from_rank("1k")


def test_dan_ranks():
    assert 1 == get_int_from_rank("1d")
    assert 9 == get_int_from_rank("9d")


def test_incorrect_ranks():
    with pytest.raises(AttributeError, match="incorrect rank*"):
        get_int_from_rank("pd")

    with pytest.raises(AttributeError, match="incorrect rank*"):
        get_int_from_rank("23")

    with pytest.raises(AttributeError, match="incorrect rank*"):
        get_int_from_rank("P")