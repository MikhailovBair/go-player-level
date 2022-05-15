import pytest

from src.parse_analyzed import get_blunder_and_mistake_val


def test_correct_order():
    blunders = list()
    mistakes = list()

    for rank in range(-14, 10):
        blunder, mistake = get_blunder_and_mistake_val(rank, path='ranks_table.csv')
        assert blunder > mistake

    for i in range(len(blunders) - 1):
        assert blunders[i] < blunders[i + 1] + 0.5
        assert mistakes[i] < mistakes[i + 1] + 0.5


def test_none_rank():
    assert (None, None) == get_blunder_and_mistake_val(None, "ranks_table.csv")


def test_incorrect_path():
    with pytest.raises(FileNotFoundError, match="No rank table"):
        get_blunder_and_mistake_val(3, 'ranks______.csv')


