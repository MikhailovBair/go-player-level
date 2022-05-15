from src.parse_analyzed import get_best_alternative_turn


def test_correct_variation():
    variations1 = [[(12, 3), (4, 5)], [(6, 7)], [(8, 9), (10, 11)]]
    assert (12, 3) == get_best_alternative_turn(variations1)

    variations2 = [[(19, 19), (8, 8), (6, 5)], [(6, 7), (5, 3)], [(8, 9), (10, 11)]]
    assert (19, 19) == get_best_alternative_turn(variations2)


def test_incorrect_variation():
    variations = [1, [(2, 3), (4, 5)]]
    assert None is get_best_alternative_turn(variations)
