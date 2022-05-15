import subprocess
import pandas as pd
from sgfmill import sgf
import re

FILE_FORMAT = '.sgf'


def convert_to_pair(turn: str):
    line = ord(turn[0]) - ord('A') + 1
    vert = int(turn[1:])
    return line, vert


def get_best_alternative_turn(variations: list):
    try:
        best_alternative = variations[0][0]
        return best_alternative
    except (IndexError, TypeError):
        return None


class Turn:
    def __init__(self, turn_number, position, score_drop, winrate_drop, variations):
        self.turn_number = turn_number
        self.position = position
        self.score_drop = score_drop
        self.winrate_drop = winrate_drop
        self.variations = variations
        self.best_alternative_turn = get_best_alternative_turn(variations)

    def __lt__(self, other):
        return self.score_drop > other.score_drop


def convert_turns_to_list(turns: list):
    list_turns = list()
    for turn in turns:
        list_turns.append(turn.turn_number)

    return list_turns


def get_numerical_variations(variations):
    num_variations = list()
    for variation in variations:
        variation_moves = variation.split()
        num_variation = list()
        for move in variation_moves:
            try:
                num_variation.append(convert_to_pair(move))
            except ValueError:
                pass
        num_variations.append(num_variation)
    return num_variations


def get_index_dan(rank):
    for i in range(len(rank)):
        if rank[i] in ['k', 'd']:
            return i
    raise AttributeError("incorrect rank {}".format(rank))


def get_int_from_rank(rank: str):
    ind = get_index_dan(rank)
    if ind < 0 or rank[0] == 'P' or not rank[:ind].isdigit():
        raise AttributeError("incorrect rank {}".format(rank))
    if rank[ind] == 'k':
        return int(-int(rank[:ind]) + 1)
    else:
        return int(rank[:ind])


def get_player_ranks(game: sgf.Sgf_game):
    try:
        black_rank = get_int_from_rank(game.get_root().get("BR"))
    except KeyError:
        black_rank = None

    try:
        white_rank = get_int_from_rank(game.get_root().get("WR"))
    except KeyError:
        white_rank = None
    return black_rank, white_rank


def get_turns_list(game: sgf.Sgf_game):
    nodes = game.get_main_sequence()
    turns_white = list()
    turns_black = list()

    for i, node in enumerate(nodes[1:]):
        position = node.get_move()[1]
        comment = node.get("C")
        try:
            winrate_drop = float(re.findall(r'([-]*\w+\.\w+)%', comment)[1])
            score_drop = float(re.findall(r'([-]*\w+\.\w+)', comment)[3])
        except IndexError:
            winrate_drop = 0
            score_drop = 0
        variations = re.findall(r'[0-9]\. [BW]([\w\s]+)\s\(', comment)
        num_variations = get_numerical_variations(variations)

        if i % 2 == 0:
            turns_black.append(Turn(turn_number=i + 1, position=position, score_drop=score_drop,
                                    winrate_drop=winrate_drop, variations=num_variations))
        else:
            turns_white.append(Turn(turn_number=i + 1, position=position, score_drop=score_drop,
                                    winrate_drop=winrate_drop, variations=num_variations))

    return turns_black, turns_white


def get_blunder_and_mistake_thresholds(rank, path):
    if rank is None:
        return None, None
    try:
        df = pd.read_csv(path, sep=',')
    except FileNotFoundError:
        raise FileNotFoundError("No rank table file")

    blunder_threshold = -float(df.loc[df['rank'] == rank]['Worst_score5'])
    mistake_threshold = -float(df.loc[df['rank'] == rank]['Worst_score10'])
    return blunder_threshold, mistake_threshold


def get_blunders_and_mistakes(turns: list, rank, path_to_thresholds):
    blunder_threshold, mistake_threshold = get_blunder_and_mistake_thresholds(rank, path_to_thresholds)
    blunders = list()
    mistakes = list()

    for turn in turns:
        if blunder_threshold is None or turn.score_drop >= blunder_threshold:
            blunders.append(turn)
        elif turn.score_drop >= mistake_threshold:
            mistakes.append(turn)

    if blunder_threshold is None:
        return blunders[:min(5, len(blunders))], list()

    return blunders, mistakes


def get_worst_errors(game: sgf.Sgf_game, path_to_thresholds):
    turns_black, turns_white = get_turns_list(game)
    turns_black.sort()
    turns_white.sort()

    rank_black, rank_white = get_player_ranks(game)
    blunders_black, mistakes_black = get_blunders_and_mistakes(turns_black, rank_black, path_to_thresholds)
    blunders_white, mistakes_white = get_blunders_and_mistakes(turns_white, rank_white, path_to_thresholds)

    dict_worst = {
        "blunders_black": convert_turns_to_list(blunders_black),
        "mistakes_black": convert_turns_to_list(mistakes_black),
        "blunders_white": convert_turns_to_list(blunders_white),
        "mistakes_white": convert_turns_to_list(mistakes_white)
    }

    return dict_worst


def get_katago_analyzed_file(source_filename):
    return source_filename[:-len(FILE_FORMAT)] + '-analyzed.sgf'


def parse_game(path_to_game, path_to_thresholds):
    subprocess.run(['analyze-sgf', "-a", "maxVisits: 1", path_to_game])
    with open(get_katago_analyzed_file(path_to_game), "rb") as f:
        game = sgf.Sgf_game.from_bytes(f.read())

    return get_worst_errors(game, path_to_thresholds)


if __name__ == "__main__":
    print(parse_game("tests/test_games/A.sgf", "ranks_table.csv"))

