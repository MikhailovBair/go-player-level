#Options: 
#--indir (-i) - the directory from which sgf files are taken
#--outdir (-o) - the directory where the cartago exhaust is placed
#--playout (-p) - playout - number of playouts used in katago
#-d - удалять файлы из indir как только они обработаются

import os
import re
import sys
import argparse

FILE_FORMAT = '.sgf'

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--indir')
    parser.add_argument('-o', '--outdir')
    parser.add_argument('-p', '--playout')
    parser.add_argument('-d', action = "store_true")
    return parser

def getKatagoJsonFile(source_filename):
    return source_filename[:-len(FILE_FORMAT)] + '.json'

def getKatagoAnalyzedFile(source_filename):
    return source_filename[:-len(FILE_FORMAT)] + '-analyzed.sgf'

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

in_directory = namespace.indir
out_directory = namespace.outdir
playout = int(namespace.playout)
delete_files = namespace.d

files = os.listdir(in_directory)

sgf_re = '.*\.sgf'
analized = '.*analyzed\.sgf'

target_files = []

for file in files:
    if re.match(sgf_re, file) is not None and re.match(analized, file) is None:
        target_files.append(file)

for target_file in target_files:
    try:
        full_filename = in_directory + '/' + target_file
        os.system('python3 get_correct_main_sequence_from_sgf.py ' + full_filename)
        os.replace(full_filename[:-4] + "_correct.sgf", full_filename)
        #os.remove(full_filename[:-4] + "_correct.sgf") 
        os.system('analyze-sgf -s -a \"maxVisits:{}\" '.format(playout) + in_directory + '/' + target_file) 
        json_file = getKatagoJsonFile(target_file)
        analyz_file = getKatagoAnalyzedFile(target_file)
        os.replace(in_directory + '/' + json_file, out_directory + '/' + json_file)
        os.replace(in_directory + '/' + analyz_file, out_directory + '/' + analyz_file)
        if delete_files:
            os.remove(in_directory + '/' + target_file) 
    except Exception as e:
        print(e)