#!/bin/bash
path_source=$1
full_path_source=$(realpath $path_source)

path_target=$2
full_path_target=$(realpath $path_target)

dirs_name=$3

filtered_games_dir=$full_path_target/$dirs_name
handicap_games_dir=$full_path_target/handicap_$dirs_name
nonjapanese_rules_games_dir=$full_path_target/nonjapan_rules_$dirs_name
badkomi_games_dir=$full_path_target/badkomi_$dirs_name


mkdir -p $filtered_games_dir
mkdir -p $handicap_games_dir
mkdir -p $nonjapanese_rules_games_dir
mkdir -p $badkomi_games_dir


ag -L 'HA\[0\]' $full_path_source | xargs cp -t $handicap_games_dir
ag -L 'RU\[Japanese\]' $full_path_source | xargs cp -t $nonjapanese_rules_games_dir
ag -L 'KM\[650\]' $full_path_source |  xargs cp -t $badkomi_games_dir
ag -l 'KM\[650\]*HA\[0\]*RU\[Japanese\]' $full_path_source | xargs cp -t $filtered_games_dir

ag -l '级' $filtered_games_dir | xargs sed -i 's/级/k/g'
ag -l '段' $filtered_games_dir | xargs sed -i 's/段/d/g' 
ag -l 'KM\[650\]' $filtered_games_dir | xargs sed -i 's/KM\[650\]/KM\[6.5\]/g' 
