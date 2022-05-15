import pytest
from src.parse_analyzed import get_katago_analyzed_file


def test_analyzed_file():
    assert "A-analyzed.sgf" == get_katago_analyzed_file("A.sgf")
    assert "/home/current-analyzed.sgf" == get_katago_analyzed_file("/home/current.sgf")
