from src.parse_analyzed import Turn, convert_turns_to_list


def test_convert_to_list():
    turn1 = Turn(1, (2, 14), 0.3, 0.4, [[(1, 2)]])
    turn2 = Turn(3, (19, 4), 0.2, 0.7, [[(1, 4), (6, 7)]])
    turn3 = Turn(5, (4, 12), 0.7, 0.3, [[(2, 5), (6, 8)]])
    turns = [turn1, turn2, turn3]
    assert [1, 3, 5] == convert_turns_to_list(turns)

