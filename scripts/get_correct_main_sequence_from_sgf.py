#!/bin/python3

import sys
from sgfmill import sgf

with open(sys.argv[1], "rb") as f:
    game = sgf.Sgf_game.from_bytes(f.read())
    main_sequence = game.get_main_sequence()
    current_node = main_sequence[0]
    while True:
        if len(current_node) > 0:
            while current_node[0] != current_node[-1]:
                current_node[0].delete()
            current_node = current_node[0]
        else:
            break

with open(sys.argv[1][:-4] + "_correct.sgf", "wb") as f:
    f.write(game.serialise())