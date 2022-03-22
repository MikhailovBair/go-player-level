import numpy as np
import pandas as pd
from tqdm import tqdm


def add_basic_stats(row, moves, suff=""):

    row['mean_deltawinrate' + suff] = np.mean(moves.winrate_delta)
    row['mean_deltascoreLead' + suff] = np.mean(moves.score_delta)
    row['mean_deltaSelfPlay' + suff] = np.mean(moves.selfplay_delta)
    row['mean_utility' + suff] = np.mean(moves.utility_delta)

    row['beautiful_percent' + suff] = np.sum([1 if x > 0 else 0 for x in moves.winrate_delta])
    row['beautifulS_percent' + suff] = np.sum([1 if x > 0 else 0 for x in moves.score_delta])

    row['dispersy_scoreLead' + suff] = np.var(moves.score_delta)


def add_advanced_stats(row, moves, suff=""):

    moves.score_delta.sort()
    moves.winrate_delta.sort()

    row['Score25p' + suff] = moves.score_delta[int(moves.cnt_moves * 0.25)]
    row['Score75p' + suff] = moves.score_delta[int(moves.cnt_moves * 0.75)]
    row['BestScoreMove'] = np.max(moves.score_delta)
    row['WorstScoreMove'] = np.min(moves.score_delta)
    row['Winrate25p'] = moves.winrate_delta[int(moves.cnt_moves * 0.25)]
    row['Winrate75p'] = moves.winrate_delta[int(moves.cnt_moves * 0.75)]

    row['Mean5WorstScoreMove'] = np.mean(moves.score_delta[-5:])
    row['Mean5BestScoreMove'] = np.mean(moves.score_delta[:5])

    row['median_scorelead'] = moves.score_delta[int(moves.cnt_moves * 0.5)]

    row['mean_deltaScore50p'] = np.mean(moves.score_delta[int(moves.cnt_moves * 0.25):int(moves.cnt_moves * 0.75)])
    row['mean_deltawinrate50p'] = np.mean(moves.winrate_delta[int(moves.cnt_moves * 0.25):int(moves.cnt_moves * 0.75)])


def get_int_from_rank(rank):
    if rank[1] == 'k':
        return -int(rank[0]) + 1
    else:
        return int(rank[0])


def get_rank_from_int(x):
    if x > 0:
        return str(x) + "d"
    else:
        return str(-x + 1) + "k"


def add_meta(row):
    row['length'] = len(row['W_move']) + len(row['B_move'])
    row['chiselka'] = get_int_from_rank(row['W_rating'])

def convert_to_lists(df):
    for i, row in tqdm(df.iterrows()):
        row['W_scoreLead'] = [float(x) for x in row['W_scoreLead'].split()]
        row['B_scoreLead'] = [float(x) for x in row['B_scoreLead'].split()]
        row['W_scoreSelfplay'] = [float(x) for x in row['W_scoreSelfplay'].split()]
        row['B_scoreSelfplay'] = [float(x) for x in row['B_scoreSelfplay'].split()]
        row['W_scoreStdev'] = [float(x) for x in row['W_scoreStdev'].split()]
        row['B_scoreStdev'] = [float(x) for x in row['B_scoreStdev'].split()]
        row['W_utility'] = [float(x) for x in row['W_utility'].split()]
        row['B_utility'] = [float(x) for x in row['B_utility'].split()]
        row['W_winrate'] = [float(x) for x in row['W_winrate'].split()]
        row['B_winrate'] = [float(x) for x in row['B_winrate'].split()]


class MovesInfo:
    def __init__(self, row, n_moves = None):
        moves_len = min(len(row['W_winrate']), len(row['B_winrate']))
        if n_moves is None:
            start_ind = 0
        else:
            start_ind = max(moves_len - n_moves - 1, 0)

        end_ind = moves_len

        self.winrate_delta = []
        self.score_delta = []
        self.utility_delta = []
        self.selfplay_delta = []
        self.cnt_moves = end_ind - start_ind
        self.move = row['W_move'].split()

        for i in range(start_ind, end_ind):
            self.winrate_delta.append(row['W_winrate'][i] - row['B_winrate'][i])
            self.score_delta.append(row['W_scoreLead'][i] - row['B_scoreLead'][i])
            self.utility_delta.append(row['W_utility'][i] - row['B_utility'][i])
            self.selfplay_delta.append(row['W_scoreSelfplay'][i] - row['B_scoreSelfplay'][i])


def add_all_game_stats(df):

    df['mean_deltawinrate'] = None
    df['mean_deltaScore50p'] = None
    df['mean_deltascoreLead'] = None
    df['dispersy_scoreLead'] = None
    df['beautiful_percent'] = None
    df['beautifulS_percent'] = None
    df['mean_utility'] = None
    df['Score25p'] = None
    df['Score75p'] = None
    df['Winrate25p'] = None
    df['Winrate75p'] = None
    df['mean_deltawinrate50p'] = None
    df['median_scorelead'] = None
    df['length'] = None
    df['chiselka'] = None
    df['mean_deltaSelfPlay'] = None
    df['delta_stddev'] = None
    df['median_delta_stddev'] = None
    df['last_stdev'] = None
    df['BestScoreMove'] = None
    df['WorstScoreMove'] = None
    df['Mean5WorstScoreMove'] = None
    df['Mean5BestScoreMove'] = None

    for i, row in tqdm(df.iterrows()):
        add_basic_stats(row, MovesInfo(row))
        add_advanced_stats(row, MovesInfo(row))
        add_meta(row)


def get_start_of_yose(margin_moves, no_change_count=5):
    '''
    Находим сколько последних ходов мы будем считать что это йосе

    Будем идти с конца по массиву количества ходов на краю, если в массиве no_change_count одинаковых чисел,
    то мы останавливаемся и говорим, что тут началось йосе
    '''
    no_change = 1
    ans = len(margin_moves)
    for i in range(len(margin_moves) - 2, -1, -1):
        if margin_moves[i] == margin_moves[i + 1]:
            no_change += 1
        else:
            no_change = 1
        if no_change >= no_change_count:
            ans = len(margin_moves) - i - 1
            break
    return ans


def reset_basic_stats(df, suff):
    df['mean_deltawinrate' + suff] = None
    df['beautiful_percent' + suff] = None
    df['beautifulS_percent' + suff] = None
    df['mean_deltascoreLead' + suff] = None
    df['mean_deltaSelfPlay' + suff] = None
    df['dispersy_scoreLead' + suff] = None
    df['mean_utility' + suff] = None


def is_marginal_move(move):
    return (move[0] == 'a' or move[0] == 'b') or (move[0] == 'r' or move[0] == 's') or\
            (move[1] == 'a' or move[1] == 'b') or (move[1] == 'r' or move[1] == 's')


def count_of_marginal_moves(moves):
    ans = np.zeros(len(moves))
    for i in range(len(moves)):
        ans[i] = is_marginal_move(moves[i])
    ans = np.cumsum(ans)
    return ans


def add_yose_stats(df):
    suff = ' yose'
    reset_basic_stats(df, suff)
    df['len_yose'] = None
    df['start_yose'] = None
    df['has_yose'] = None
    for i, row in tqdm(df.iterrows()):
        marginal_moves = count_of_marginal_moves(row['W_move'].split())
        n_moves = get_start_of_yose(marginal_moves, 10)
        add_basic_stats(row, MovesInfo(row, n_moves), suff)
        row['len_yose'] = n_moves
        row['start_yose'] = len(row['W_move'].split()) - n_moves
        row['has_yose'] = row['start_yose'] != 0


def delta_moves(a, b):
    return abs(ord(a[0]) - ord(b[0])) + abs(ord(a[1]) - ord(b[1]))


def get_distance_of_moves(moves):
    ans = np.zeros(len(moves) - 1)
    for i in range(1, len(moves)):
        ans[i - 1] = delta_moves(moves[i], moves[i - 1])
    return ans


def get_distance_from_enemy(my_moves, enemy_moves):
    ans = np.zeros(min(len(my_moves), len(enemy_moves)))
    for i in range(min(len(my_moves), len(enemy_moves))):
        ans[i] = delta_moves(my_moves[i], enemy_moves[i])
    return ans


def more_than(x, k):
  if x >= k:
    return True
  else:
    return False


def add_last_moves_stats(df, n_moves, suff=None):
    if suff is None:
        suff = " " + str(n_moves)
    reset_basic_stats(df, suff)
    for i, row in tqdm(df.iterrows()):
        add_basic_stats(row, MovesInfo(row, n_moves), suff)


def add_dist_stats_to_row(row):
    dist = get_distance_of_moves(row['W_move'].split())
    dist_enemy = get_distance_from_enemy(row['W_move'].split(), row['B_move'].split())
    dist.sort()

    row['mean_dist'] = np.mean(dist)
    row['dispersy_dist'] = np.var(dist)
    row['median_dist'] = dist[len(dist) // 2]
    row['percent_p10'] = np.sum([more_than(x, 10) for x in dist])
    row['percent_p5'] = np.sum([more_than(x, 5) for x in dist])
    row['percent_p20'] = np.sum([more_than(x, 20) for x in dist])

    row['mean_dist_from_enemy'] = np.mean(dist_enemy)
    row['dispersy_dist_from_enemy'] = np.var(dist_enemy)


def add_dist_stats(df):
    df['mean_dist'] = None
    df['dispersy_dist'] = None
    df['percent_p10'] = None
    df['percent_p5'] = None
    df['percent_p20'] = None

    df['mean_dist_from_enemy'] = None
    df['dispersy_dist_from_enemy'] = None
    df['median_dist'] = None

    for i, row in tqdm(df.iterrows()):
        add_dist_stats_to_row(row)


def delete_non_scalar_parameters(df):
    df.drop(['W_rating', 'B_rating', 'W_move', 'B_move', 'W_scoreLead', 'B_scoreLead', 'W_scoreSelfplay',
             'B_scoreSelfplay', 'W_scoreStdev',	'B_scoreStdev',	'W_utility', 'B_utility', 'W_visits', 'B_visits',
             'W_winrate', 'B_winrate'], axis=1, inplace=True)


def get_feature_df(df):
    convert_to_lists(df)
    add_all_game_stats(df)
    add_yose_stats(df)
    add_last_moves_stats(df, 10)
    add_last_moves_stats(df, 20)
    add_dist_stats(df)
    delete_non_scalar_parameters(df)
    return df


