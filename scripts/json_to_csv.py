import json
import csv
import glob

def get_ratings(line):
    ind = line.find('BR')
    ind2 = line.find(']', ind)
    b_rating = line[ind+3: ind2]
    
    ind = line.find('WR')
    ind2 = line.find(']', ind)
    w_rating = line[ind+3: ind2]
    return w_rating, b_rating

def file_to_row(name):
    # инициализация хранилища
    features = ['scoreLead', 'scoreSelfplay', 'scoreStdev', 'utility', 'visits', 'winrate']
    stats = dict()
    stats['B'] = dict()
    stats['W'] = dict()
    for feature in features:
        stats['B'][feature] = []
        stats['W'][feature] = []
    # чтение файла
    with open(name, 'r') as f:
        lines = f.read().split('\n')
    
    # обработка каждого хода
    for line in lines[1:]:
        if len(line) < 10:
            break
        json_line = json.loads(line)['rootInfo']
        color = json_line['currentPlayer']
        for feature in features:
            stats[color][feature].append(json_line[feature])
    row = []
    ratings = get_ratings(lines[0])
    row.append(ratings[0])
    row.append(ratings[1])
    
    # сохраняем последовательность статистик в виде строки
    for feature in features:
        stat = map(str, stats['W'][feature])
        row.append(' '.join(stat))
        stat = map(str, stats['B'][feature])
        row.append(' '.join(stat))
    return row



def create_csv(filename, rows):
    columns = ['W_rating', 'B_rating','W_scoreLead', 'B_scoreLead','W_scoreSelfplay', 'B_scoreSelfplay',
           'W_scoreStdev', 'B_scoreStdev', 'W_utility', 'B_utility', 'W_visits', 'B_visits',
           'W_winrate', 'B_winrate']
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

rows = []
filenames = glob.glob('*.json')

for file in filenames:
    rows.append(file_to_row(file))

create_csv('data.csv', rows)