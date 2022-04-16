import sys
sys.path.insert(1, '../code')
import features
import pandas as pd
import argparse
from tqdm import tqdm
import numpy as np


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--table')
    return parser

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])
table_path = namespace.table
predictions = pd.read_csv(table_path)
rz = dict({'WW': [], 'WB': [], 'BB': [], 'BW' : []})
rz_real = []
for i, row in tqdm(predictions.iterrows()):
    if row['W_real_rating'] is not None and row['B_predicted_rating'] is not None:
        try:
            rz_real.append(abs(features.get_int_from_rank(row['W_real_rating'])
                                                  - features.get_int_from_rank(row['B_real_rating'])))
        except Exception:
            print(row['W_real_rating'])    
    for color in ['W', 'B']:
        for pred_color in ['W', 'B']:
            if row[color + '_real_rating'] is not None and row[pred_color + '_predicted_rating'] is not None:
                try: 
                  rz[color + pred_color].append(abs(features.get_int_from_rank(row[color + '_real_rating'])
                                                  - features.get_int_from_rank(row[pred_color + '_predicted_rating'])))
                except Exception:
                  print(row[color + '_real_rating'])
print(len(list(rz['WW']) + list(rz['BB'])))
print('MAE при предсказании игр с известным рейтингом: ', np.mean(list(rz['WW']) + list(rz['BB'])))
print('MAE при предсказании игр с известным рейтингом (WB и BW): ', np.mean(list(rz['WB']) + list(rz['BW'])))
print('Средняя разница в рангах в исходном рейтинге: ', np.mean(rz_real))

