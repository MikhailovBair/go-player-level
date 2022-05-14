import json
import csv
import sys
import os
import argparse


def get_result(line):
    ind = line.find('RE[')
    if line[ind + 3] == 'W':
        return "-1"
    else:
        if line[ind + 3] == 'B':
            return "1"
        else:
            return '?'


def get_nickname(line):
    indb = line.find('PB[')
    indbe = line.find(']', indb)
    indw = line.find('PW[')
    indwe = line.find(']', indw)

    b_nickname = line[indb+3: indbe]
    w_nickname = line[indw+3: indwe]

    return w_nickname, b_nickname


def get_ratings(line):
    ind = line.find('BR[')
    ind2 = line.find(']', ind)
    b_rating = line[ind+3: ind2]
    ind = line.find('WR[')
    ind2 = line.find(']', ind)
    w_rating = line[ind+3: ind2]
    return w_rating, b_rating


def get_moves(line):
    moves = []
    ind = line.find(';B[')
    line = line[ind+3:]

    while ind != -1:
        moves.append(line[:2])
        
        ind = line.find('[')
        line = line[ind+1:]
    return moves


def file_to_row(name):
    # инициализация хранилища
    features = ['moves', 'scoreLead', 'scoreSelfplay', 'scoreStdev', 'utility', 'winrate']
    stats = dict()
    stats['B'] = dict()
    stats['W'] = dict()
    error = ""
    for feature in features:
        stats['B'][feature] = []
        stats['W'][feature] = []
    # чтение файла
    with open(name, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    
    or_lines = dict()
    for line in lines[1:-1]:
        key = json.loads(line)['turnNumber']
        or_lines[key] = json.loads(line)

    # обработка каждого хода
    moves = get_moves(lines[0])
    for key in sorted(list(or_lines.keys()))[:-1]:
        json_line = or_lines[key]['rootInfo']
        color = json_line['currentPlayer']
        for feature in features[1:]:
            stats[color][feature].append(json_line[feature])
        if key < len(moves):
            stats[color]['moves'].append(moves[key])
        else:
            error = "Index of turn out of range"
    row = []
    ratings = get_ratings(lines[0])
    row.append(ratings[0])
    row.append(ratings[1])
    nicknames = get_nickname(lines[0])
    row.append(nicknames[0])
    row.append(nicknames[1])
    row.append(get_result(lines[0]))
    # сохраняем последовательность статистик в виде строки
    for feature in features:
        stat = map(str, stats['W'][feature])
        row.append(' '.join(stat))
        stat = map(str, stats['B'][feature])
        row.append(' '.join(stat))
    row.append(name[:-len(".json")])
    row.append(error)
    return row


def create_csv(filename, rows):
    columns = ['W_rating', 'B_rating', 'W_nickname', 'B_nickname', 'Result', 'W_move', 'B_move',
            'W_scoreLead', 'B_scoreLead', 'W_scoreSelfplay', 'B_scoreSelfplay',
           'W_scoreStdev', 'B_scoreStdev', 'W_utility', 'B_utility',
           'W_winrate', 'B_winrate', 'game_id', 'error']
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
    with open(filename, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--indir')
    parser.add_argument('-o', '--out_table')
    return parser

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

in_directory = namespace.indir
out_table = namespace.out_table

filenames = os.listdir(in_directory)

rows = []

for file in filenames:
    if file[-5:] == ".json":
        rows.append(file_to_row(in_directory + '/' + file))

create_csv(out_table, rows)
