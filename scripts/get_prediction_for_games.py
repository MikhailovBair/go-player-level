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


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--indir')
    parser.add_argument('-o', '--outdir')
    parser.add_argument('-m', '--model')
    parser.add_argument('-c', '--config_model')
    return parser


def get_rnn_regression_model(config_path):
    config = load_model(config_path)
    model = models.RnnKerasRunner(model=config, sequence_len=250)
    return model


def get_rnn_classifier_model(config_path):
    config = load_model(config_path)
    model = models.RnnKerasClassifierRunner(min_rank=-15, max_rank=9, model=config, sequence_len=250)
    return model


def get_model(model_type, config_path):
    getters = dict({
        'rnn_regression': get_rnn_regression_model,
        'rnn_classifier': get_rnn_classifier_model,
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

data = get_data(in_directory, out_directory)
df_to_pred = pd.concat([features.get_df_with_lists(data.copy(), player='W'), features.get_df_with_lists(data.copy(), player='B')])
model = get_model(model_type, config_path)
df_to_pred["prediction"] = model.predict(df_to_pred)

games_res = defaultdict(dict)

for i, row in tqdm(df_to_pred.iterrows()):
    player = features.player_from_int(row['color'])

    games_res[row['game_id']][player + '_real_rating'] = \
        features.get_rank_from_int(row['rank']) if row['rank'] is not None else None
    games_res[row['game_id']][player + '_predicted_rating'] = features.get_rank_from_int(row['prediction'])
    games_res[row['game_id']]['id'] = row['game_id']
    games_res[row['game_id']][player + '_nickname'] = row[player + '_nickname']

result_df = pd.DataFrame(columns=['game_id', 'W_real_rating', 'B_real_rating', 'W_predicted_rating',
                                  'B_predicted_rating', 'W_nickname', 'B_nickname'])
for result in games_res.values():
    result_df = result_df.append(result, ignore_index=True)
result_df.to_csv(out_directory + '/result.csv')