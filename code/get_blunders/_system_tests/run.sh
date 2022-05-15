!#bin/bash

gunicorn --bind :5000 --workers 1 --threads 8 --timeout 0 --chdir "$PWD/../.."  main:app &
sleep 5 
python3 ./_system_test.py