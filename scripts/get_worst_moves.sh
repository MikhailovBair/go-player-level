#!/bin/bash
path_source=$1
full_path_source=$(realpath $path_source)

# analyze-sgf -a 'maxVisits:10' $full_path_source
path_to_analyze=${full_path_source%.sgf}-analyzed.sgf
black_bad_moves=$(cat $path_to_analyze | grep -o -P "Top 10 win rate drops: \K.*" | grep -o -P "#\K[0-9]*" | head -10)
white_bad_moves=$(cat $path_to_analyze | grep -o -P "Top 10 win rate drops: \K.*" | grep -o -P "#\K[0-9]*" | tail -10)

alternative_turns=$(cat A-analyzed.sgf | grep -P -o "^1\. .\K...|C.Move")
cleared_alternative_turn=""
previous_cmove="0"

for current in $alternative_turns
do
	if [[ "$current" == *Move* ]]; then
		if [[ "$previous_cmove" == "1" ]]; then
			cleared_alternative_turn="${cleared_alternative_turn} none"
		fi
		previous_cmove="1"
	else
		previous_cmove="0"
		cleared_alternative_turn="${cleared_alternative_turn} ${current}"
	fi
done

arr_cleared_alternative_turn=($cleared_alternative_turn)
recommended_black=""
recommended_white=""

for turn in $black_bad_moves
do 
	move=${arr_cleared_alternative_turn[turn - 1]}
	for old_move in $recommended_black
	do
		if [[ "$move" == "$old_move" ]]; then
			move="none"
		fi
	done

	if ! [[ "$move" = "none" ]]; then
		echo $turn 
	fi
	recommended_black="${recommended_black} ${move}"
done 


echo ' '

for turn in $white_bad_moves
do  
	move=${arr_cleared_alternative_turn[turn - 1]}
	for old_move in $recommended_black
	do
		if [[ "$move" == "$old_move" ]]; then
			move="none"
		fi
	done

	if ! [[ "$move" = "none" ]]; then
		echo $turn 
	fi

	recommended_white="${recommended_white} ${move}"
done 
