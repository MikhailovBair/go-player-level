from src.parse_analyzed import Turn


def test_init():
    turn = Turn(1, (2, 3), 0.3, 0.4, [[(1, 2)]])


def test_sorting():
    turn1 = Turn(1, (2, 3), 0.3, 0.4, [[(1, 2)]])
    turn2 = Turn(3, (3, 4), 0.2, 0.7, [[(2, 4), (6, 7)]])
    turn3 = Turn(5, (4, 8), 0.7, 0.7, [[(2, 1), (6, 8)]])
    turns = [turn1, turn2, turn3]
    turns.sort()
    assert turns == [turn3, turn1, turn2]