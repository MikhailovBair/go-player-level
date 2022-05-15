from src.parse_analyzed import get_blunders_and_mistakes, Turn


def test_correct_rank():
    turn1 = Turn(1, (2, 3), 100, 0.4, [[(1, 2)]])
    turn2 = Turn(3, (3, 4), 200, 0.7, [[(2, 5), (6, 7)]])
    turn3 = Turn(5, (4, 8), -300, 0.7, [[(2, 3), (6, 8)]])
    turns = [turn1, turn2, turn3]

    blunders, mistakes = get_blunders_and_mistakes(turns, 1, "../ranks_table.csv")
    assert turn1 in blunders
    assert turn2 in blunders
    assert turn3 not in blunders


def test_none_rank():
    turn1 = Turn(1, (2, 3), 0.1, 0.4, [[(1, 2)]])
    turn2 = Turn(3, (3, 4), 0.2, 0.7, [[(2, 5), (6, 7)]])
    turn3 = Turn(5, (4, 8), 0.7, 0.7, [[(2, 3), (6, 8)]])
    turn4 = Turn(7, (4, 10), 0.7, 0.7, [[(2, 3), (6, 8)]])
    turn5 = Turn(9, (4, 8), 0.7, 0.7, [[(2, 3), (6, 8)]])
    turn6 = Turn(11, (4, 6), 0.7, 0.7, [[(1, 3), (5, 8)]])
    turns = [turn1, turn2, turn3, turn4, turn5, turn6]

    blunders, mistakes = get_blunders_and_mistakes(turns, None, "../ranks_table.csv")
    assert 5 == len(blunders)
    assert 0 == len(mistakes)

