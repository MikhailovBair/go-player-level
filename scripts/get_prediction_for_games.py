import os
import sys

sys.path.insert(1, '../code')

import argparse
import models
import features
from keras.models import load_model
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
import numpy as np
import json

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--indir')
    parser.add_argument('-o', '--outdir')
    parser.add_argument('-m', '--model')
    parser.add_argument('-c', '--config_model')
    parser.add_argument('-j', '--need_json', action = "store_true")
    return parser


def get_rnn_regression_model(config_path):
    config = load_model(config_path)
    model = models.RnnKerasRunner(model=config, sequence_len=250)
    return model


def get_rnn_classifier_model(config_path):
    config = load_model(config_path)
    model = models.RnnKerasClassifierRunner(min_rank=-15, max_rank=9, model=config, sequence_len=250)
    return model

def get_file_and_dir(path):
    last_ch = max(path.rfind('/'), path.rfind(r'\x'[0]))
    return path[:last_ch + 1], path[last_ch + 1:]    
    
    
def erase_filename(path):
    return get_file_and_dir(path)[0]
    
    
def get_filename(path):
    return get_file_and_dir(path)[1]
    
    
def get_combined_model(config_path):
    config = open(config_path).readlines()
    models_dir = erase_filename(config_path)
    features = config[0].strip().replace("'", "").split(', ')
    W_model = models.RnnKerasRunner(model = load_model(models_dir + config[1].strip()), sequence_len=150, features=features)
    B_model = models.RnnKerasRunner(model = load_model(models_dir + config[2].strip()), sequence_len=150, features=features)
    model = models.TwoModelsCombiner(W_model, B_model)
    return model    


def get_model(model_type, config_path):
    getters = dict({
        'rnn_regression': get_rnn_regression_model,
        'rnn_classifier': get_rnn_classifier_model,
        'combined_model': get_combined_model,
    })
    if model_type not in getters.keys():
        print('Wrong model type! \"{}\" type does not exist!'.format(model_type))
        exit(0)
    return getters[model_type](config_path)


def get_data(in_directory, out_directory):
    temp_dir = out_directory + '/temp'
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    os.system('python3 analyze_dir_katago.py --indir \"{}\" --outdir \"{}\" --playout 1'.format(in_directory, temp_dir))
    table_features_name = temp_dir + '/data.csv'
    os.system('python3 json_to_csv.py --indir \"{}\" --out_table \"{}\"'.format(temp_dir, table_features_name))
    data = pd.read_csv(table_features_name)
    return data


parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

in_directory = namespace.indir
out_directory = namespace.outdir
model_type = namespace.model
config_path = namespace.config_model
need_json = namespace.need_json

data = get_data(in_directory, out_directory)
df_to_pred = pd.concat([features.get_df_with_lists(data.copy(), player='W'), features.get_df_with_lists(data.copy(), player='B')])
model = get_model(model_type, config_path)
df_to_pred["prediction"] = model.predict(df_to_pred)

games_res = defaultdict(dict)
mz = dict({'WB':[], 'BB':[], 'BW':[], 'WW':[]})
for i, row in tqdm(df_to_pred.iterrows()):
    player = features.player_from_int(row['color'])

    games_res[row['game_id']][player + '_real_rating'] = \
        features.get_rank_from_int(row['rank']) if row['rank'] is not None else None
    games_res[row['game_id']][player + '_predicted_rating'] = features.get_rank_from_int(row['prediction'])
    games_res[row['game_id']]['id'] = get_filename(row['game_id'])
    games_res[row['game_id']][player + '_nickname'] = row[player + '_nickname']


player_rating = defaultdict(list)
    
for row in games_res.values():    
    for color in ['W', 'B']:
        if row[color + '_predicted_rating'] is not None:
            player_rating[row[color + '_nickname']].append(features.get_int_from_rank(row[color + '_predicted_rating']))
    for real_color in ['W', 'B']:
        if row[real_color + '_real_rating'] is not None:
            for color_to_pred in ['W', 'B']:
                if row[color_to_pred + '_predicted_rating'] is not None:
                    mz[real_color + color_to_pred].append(abs(features.get_int_from_rank(row[color_to_pred + '_predicted_rating']) - features.get_int_from_rank(row[real_color + '_real_rating'])))


result_df = pd.DataFrame(columns=['game_id', 'W_real_rating', 'B_real_rating', 'W_predicted_rating',
                                  'B_predicted_rating', 'W_nickname', 'B_nickname'])
                                  
for result in games_res.values():
    if need_json:
        json_ans = {
            'W_rank': result['W_predicted_rating'],
            'B_rank': result['B_predicted_rating']
        }
        with open(out_directory + '/' + result['id'] + '.json', 'w') as f:
            json.dump(json_ans, f)
    result_df = result_df.append(result, ignore_index=True)
    
    
players_pd = pd.DataFrame(columns=['nickname', 'games_played', 'mean_predicted_rating', 'var_predicted_rating', 'min_pred_rating', 'max_pred_rating'])    
for nick, ratings in player_rating.items():
    row = {
        'nickname': nick,
        'games_played': len(ratings),
        'mean_predicted_rating': features.get_rank_from_int(round(np.mean(ratings))),
        'var_predicted_rating': np.var(ratings),
        'min_pred_rating': features.get_rank_from_int(round(np.min(ratings))),
        'max_pred_rating': features.get_rank_from_int(round(np.max(ratings))),
    };
    players_pd = players_pd.append(row, ignore_index=True)
    
for k, v in mz.items():
    print(k, np.mean(v))
result_df.to_csv(out_directory + '/result.csv')
players_pd.to_csv(out_directory + '/players_df.csv')