from src.parse_analyzed import get_numerical_variations, convert_to_pair


def test_correct():
    variations1 = ["B3 D3", "C8 B5"]
    assert [[(2, 3), (4, 3)], [(3, 8), (2, 5)]] == get_numerical_variations(variations1)

    variations2 = ["C14 D13"]
    assert [[(3, 14), (4, 13)]] == get_numerical_variations(variations2)


def test_incorrect():
    variation = ["C3 P", "E3 M14", "D8"]
    assert [[(3, 3)], [(5, 3), (13, 14)], [(4, 8)]] == get_numerical_variations(variation)