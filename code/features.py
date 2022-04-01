import numpy as np
import pandas as pd
from tqdm import tqdm


def add_basic_stats(row, moves, pref=""):
    row[pref + 'winrate_mean'] = np.mean(moves.winrate_delta)
    row[pref + 'score_mean'] = np.mean(moves.score_delta)
    row[pref + 'score_var'] = np.var(moves.score_delta)
    row[pref + 'selfplay_mean'] = np.mean(moves.selfplay_delta)
    row[pref + 'utility_mean'] = np.mean(moves.utility_delta)
    row[pref + 'winrate_beauty_percent'] = np.mean([x > 0 for x in moves.winrate_delta])
    row[pref + 'score_beauty_percent'] = np.mean([x > 0 for x in moves.score_delta])


def add_advanced_stats(row, moves, pref=""):
    moves.score_delta.sort()
    moves.winrate_delta.sort()

    row[pref + 'score25p'] = moves.score_delta[int(moves.cnt_moves * 0.25)]
    row[pref + 'score75p'] = moves.score_delta[int(moves.cnt_moves * 0.75)]
    row[pref + 'score_max'] = np.max(moves.score_delta)
    row[pref + 'score_min'] = np.min(moves.score_delta)
    row[pref + 'winrate25p'] = moves.winrate_delta[int(moves.cnt_moves * 0.25)]
    row[pref + 'winrate75p'] = moves.winrate_delta[int(moves.cnt_moves * 0.75)]

    row[pref + 'score_five_best_mean'] = np.mean(moves.score_delta[-5:])
    row[pref + 'score_five_worst_mean'] = np.mean(moves.score_delta[:5])

    row[pref + 'stddev_last'] = moves.stddev_delta[-1]
    moves.stddev_delta.sort()
    row[pref + 'stddev_mean'] = np.mean(moves.stddev_delta)
    row[pref + 'stddev50p'] = moves.stddev_delta[int(moves.cnt_moves * 0.5)]

    row[pref + 'score50p'] = moves.score_delta[int(moves.cnt_moves * 0.5)]

    row[pref + 'winrate_midmean'] = np.mean(
        moves.winrate_delta[int(moves.cnt_moves * 0.25):int(moves.cnt_moves * 0.75)])
    row[pref + 'score_midmean'] = np.mean(moves.score_delta[int(moves.cnt_moves * 0.25):int(moves.cnt_moves * 0.75)])


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
    if row['Result'] == '?':
        row['game_result'] = 0
    else:
        row['game_result'] = int(row['Result'])
    row['rank'] = get_int_from_rank(row['W_rating'])
    row['game_length'] = len(row['W_move']) + len(row['B_move'])


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
    def __init__(self, row, n_moves=None, player='W'):
        enemy = 'B' if player == 'W' else 'W'
        moves_len = min(len(row[player + '_winrate']), len(row[enemy + '_winrate']))
        if n_moves is None:
            start_ind = 0
        else:
            start_ind = max(moves_len - n_moves - 1, 0)

        end_ind = moves_len
        self.winrate_delta = np.array(row[player + '_winrate'][start_ind:end_ind]) - np.array(
            row[enemy + '_winrate'][start_ind:end_ind])
        self.score_delta = np.array(row[player + '_scoreLead'][start_ind:end_ind]) - np.array(
            row[enemy + '_scoreLead'][start_ind:end_ind])
        self.utility_delta = np.array(row[player + '_utility'][start_ind:end_ind]) - np.array(
            row[enemy + '_utility'][start_ind:end_ind])
        self.selfplay_delta = np.array(row[player + '_scoreSelfplay'][start_ind:end_ind]) - np.array(
            row[enemy + '_scoreSelfplay'][start_ind:end_ind])
        self.stddev_delta = np.array(row[player + '_scoreStdev'][start_ind:end_ind]) - np.array(
            row[enemy + '_scoreStdev'][start_ind:end_ind])
        self.move = row[player + '_move'].split()
        self.cnt_moves = end_ind - start_ind


def add_all_game_stats(df):
    df['winrate_mean'] = None
    df['score_midmean'] = None
    df['score_mean'] = None
    df['score_var'] = None
    df['winrate_beauty_percent'] = None
    df['score_beauty_percent'] = None
    df['utility_mean'] = None
    df['score25p'] = None
    df['score75p'] = None
    df['winrate25p'] = None
    df['winrate75p'] = None
    df['winrate_midmean'] = None
    df['score50p'] = None
    df['game_length'] = None
    df['rank'] = None
    df['game_result'] = None
    df['selfplay_mean'] = None
    df['stddev_mean'] = None
    df['stddev50p'] = None
    df['stddev_last'] = None
    df['score_max'] = None
    df['score_min'] = None
    df['score_five_best_mean'] = None
    df['score_five_worst_mean'] = None

    for i, row in tqdm(df.iterrows()):
        add_meta(row)
        add_basic_stats(row, MovesInfo(row))
        add_advanced_stats(row, MovesInfo(row))


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


def reset_basic_stats(df, pref):
    df[pref + 'winrate_mean'] = None
    df[pref + 'winrate_beauty_percent'] = None
    df[pref + 'score_beauty_percent'] = None
    df[pref + 'score_mean'] = None
    df[pref + 'selfplay_mean'] = None
    df[pref + 'score_var'] = None
    df[pref + 'utility_mean'] = None


def is_marginal_move(move):
    return (move[0] == 'a' or move[0] == 'b') or (move[0] == 'r' or move[0] == 's') or \
           (move[1] == 'a' or move[1] == 'b') or (move[1] == 'r' or move[1] == 's')


def count_of_marginal_moves(moves):
    ans = np.zeros(len(moves))
    for i in range(len(moves)):
        ans[i] = is_marginal_move(moves[i])
    ans = np.cumsum(ans)
    return ans


def add_yose_stats(df):
    pref = 'yose_'
    reset_basic_stats(df, pref)
    df['yose_length'] = None
    df['yose_start'] = None
    df['yose_has'] = None
    for i, row in tqdm(df.iterrows()):
        marginal_moves = count_of_marginal_moves(row['W_move'].split())
        n_moves = get_start_of_yose(marginal_moves, 10)
        add_basic_stats(row, MovesInfo(row, n_moves), pref)
        row['yose_length'] = n_moves
        row['yose_start'] = len(row['W_move'].split()) - n_moves
        row['yose_has'] = row['yose_start'] != 0


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


def add_last_moves_stats(df, n_moves, pref=None):
    if pref is None:
        pref = str(n_moves) + "_"
    reset_basic_stats(df, pref)
    for i, row in tqdm(df.iterrows()):
        add_basic_stats(row, MovesInfo(row, n_moves), pref)


def add_dist_stats_to_row(row):
    dist = get_distance_of_moves(row['W_move'].split())
    dist_enemy = get_distance_from_enemy(row['W_move'].split(), row['B_move'].split())
    dist.sort()

    row['dist_mean'] = np.mean(dist)
    row['dist_var'] = np.var(dist)
    row['dist_median'] = dist[len(dist) // 2]
    row['dist_procent_more_than_10'] = np.mean([x > 10 for x in dist])
    row['dist_procent_more_than_5'] = np.mean([x > 5 for x in dist])
    row['dist_procent_more_than_20'] = np.mean([x > 20 for x in dist])

    row['dist_from_enemy_mean'] = np.mean(dist_enemy)
    row['dist_from_enemy_var'] = np.var(dist_enemy)


def add_dist_stats(df):
    df['dist_mean'] = None
    df['dist_var'] = None
    df['dist_median'] = None
    df['dist_procent_more_than_5'] = None
    df['dist_procent_more_than_10'] = None
    df['dist_procent_more_than_20'] = None

    df['dist_from_enemy_mean'] = None
    df['dist_from_enemy_var'] = None

    for i, row in tqdm(df.iterrows()):
        add_dist_stats_to_row(row)


def delete_non_scalar_parameters(df):
    df.drop(['W_rating', 'B_rating', 'W_move', 'B_move', 'W_scoreLead', 'B_scoreLead', 'W_scoreSelfplay',
             'B_scoreSelfplay', 'W_scoreStdev', 'B_scoreStdev', 'W_utility', 'B_utility', 'W_visits', 'B_visits',
             'W_winrate', 'B_winrate', 'Result'], axis=1, inplace=True)


def add_delta_lists_to_row(row, moves):
    row['winrate'] = moves.winrate_delta
    row['score'] = moves.score_delta
    row['winrate_sqr'] = np.array([x ** 2 for x  in moves.winrate_delta])
    row['score_sqr'] = np.array([x ** 2 for x  in moves.score_delta])
    row['utility'] = moves.utility_delta
    row['selfplay'] = moves.selfplay_delta
    row['stddev'] = moves.stddev_delta
    row['dist_from_prev'] = get_distance_of_moves(moves.move)
    row['dist_more_5'] = [int(x > 5) + 1 for x in row['dist_from_prev']]


def add_lists_to_df(df):
    df['winrate'] = None
    df['score'] = None
    df['utility'] = None
    df['selfplay'] = None
    df['stddev'] = None
    df['dist_from_prev'] = None
    df['rank'] = None
    df['game_length'] = None
    df['score_sqr'] = None
    df['winrate_sqr'] = None
    df['dist_more_5'] = None
    for i, row in tqdm(df.iterrows()):
        add_meta(row)
        add_delta_lists_to_row(row, MovesInfo(row))


def get_feature_df(df):
    convert_to_lists(df)
    add_all_game_stats(df)
    add_yose_stats(df)
    add_last_moves_stats(df, 10)
    add_last_moves_stats(df, 20)
    add_dist_stats(df)
    delete_non_scalar_parameters(df)
    return df


def get_df_with_lists(df):
    convert_to_lists(df)
    add_all_game_stats(df)
    add_last_moves_stats(df, 20)
    add_dist_stats(df)
    add_lists_to_df(df)
    delete_non_scalar_parameters(df)
    return df
