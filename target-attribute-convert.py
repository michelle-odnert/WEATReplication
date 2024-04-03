import os
import json
import argparse

# reads words from each file and return as list
def create_word_list(path):
    with open(path, 'r') as file:
        return [word.strip().lower() for word in file if word.strip()]
    
# build dictionary where key is name set (from file name) and dict contains file words
def create_weat_dict(weat_dir, output_path):
    weat_dict = {}

    # Iterate over files in directory to build dictionary
    for data_name in os.listdir(weat_dir):
        path = os.path.join(weat_dir, data_name)

        if os.path.abspath(output_path):
            continue

        