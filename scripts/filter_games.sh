#!/bin/bash
path_source=$1
full_path_source=$(realpath $path_source)

path_target=$2
full_path_target=$(realpath $path_target)

dirs_name=$3

filtered_games_dir=$full_path_target/games/$dirs_name
handicap_games_dir=$full_path_target/bad_games/handicap/handicap_$dirs_name
nonjapanese_rules_games_dir=$full_path_target/bad_games/nonjapan_rules/nonjapan_rules_$dirs_name
badkomi_games_dir=$full_path_target/bad_games/bad_komi/bad_komi_$dirs_name

# Deleting games with bad nicks
ag -l  "PW\[([^\[\]]*?)\[[^\s]" $full_path_source | xargs rm 2> /dev/null
ag -l  "PW\[([^\[\]]*?)\][^\s]" $full_path_source | xargs rm 2> /dev/null
ag -l  "PB\[([^\[\]]*?)\[[^\s]" $full_path_source | xargs rm 2> /dev/null
ag -l  "PB\[([^\[\]]*?)\][^\s]" $full_path_source | xargs rm 2> /dev/null
ag -l  "\[\["                   $full_path_source | xargs rm 2> /dev/null
ag -l  "\]\]"                   $full_path_source | xargs rm 2> /dev/null
ag -l  "PW\[\]"                 $full_path_source | xargs rm 2> /dev/null
ag -l  "PB\[\]"                 $full_path_source | xargs rm 2> /dev/null

mkdir -p $filtered_games_dir
mkdir -p $handicap_games_dir
mkdir -p $nonjapanese_rules_games_dir
mkdir -p $badkomi_games_dir

# Move games to dirs
ag -L 'HA\[0\]' $full_path_source | xargs mv --target-directory=$handicap_games_dir
# ag -L 'RU\[Japanese\]' $full_path_source | xargs mv --target-directory=$nonjapanese_rules_games_dir
# ag -L 'KM\[(650|0)\]' $full_path_source |  xargs mv --target-directory=$badkomi_games_dir
ag -l 'HA\[0\]' $full_path_source | xargs mv --target-directory=$filtered_games_dir


# Fix rank and komi
ag -l '级' $filtered_games_dir | xargs sed -i 's/级/k/g'
ag -l '段' $filtered_games_dir | xargs sed -i 's/段/d/g' 
ag -l 'KM\[650\]' $filtered_games_dir | xargs sed -i 's/KM\[650\]/KM\[6.5\]/g' 
ag -l 'KM\[0\]' $filtered_games_dir | xargs sed -i 's/KM\[0\]/KM\[6.5\]/g'


less_games_small_dir=$full_path_target/less_games/less_$dirs_name
mkdir -p $less_games_small_dir
ag -l "" $filtered_games_dir | head -100000 | xargs mv --target-directory=$less_games_small_dir

# Extracting 10'000 games
filtered_games_small_dir=$full_path_target/small_games/small_$dirs_name
mkdir -p $filtered_games_small_dir
ag -l "" $filtered_games_dir | head -10000 | xargs mv --target-directory=$filtered_games_small_dir