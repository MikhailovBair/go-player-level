filter_games.sh 

Скрипт для фильтрации игр в Го в формате .sgf. Отбирает игры без форы, с коми 6.5 и японскими правилами.

Для работы скрипта потребуется установить утилиту Silver Searcher: apt-get install silversearcher-ag

Запуск: ./filter_games.sh PATH/TO/GAMES PATH/TO/TARGET DIR_NAME

По итогу создается 4 папки в PATH/TO/TARGET:
handicap_DIR_NAME -- Игры с форой

nonjapan_rules_DIR_NAME -- Игры не по японским правилам

badkomi_DIR_NAME -- Игры не с коми 6.6

DIR_NAME -- Искомые игры