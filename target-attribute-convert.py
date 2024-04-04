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
        
    # remove underscore and file extension
    key = os.path.splitext(data_name)[0].replace('_', '')
    values = create_word_list(path)
    weat_dict[key] = {'words': values}

    weat_dict['flowers_vs_insects_pleasant_vs_unpleasant'] = {
        'method': 'weat',
        'X_key': 'flowers',
        'Y_key': 'insects',
        'A_key': 'pleasant',
        'B_key': 'unpleasant',
        'targets': 'flowers vs insects',
        'attributes': 'pleasant vs unpleasant',
    }

    
    # target: instruments vs. weapons
    # attributes: pleasant vs. unpleasant
    weat_dict['instruments_vs_weapons_pleasant_vs_unpleasant'] = {
        'method': 'weat',
        'X_key': 'instruments',
        'Y_key': 'weapons',
        'A_key': 'pleasant',
        'B_key': 'unpleasant',
        'targets': 'instruments vs weapons',
        'attributes': 'pleasant vs unpleasant',
    }

    # European-American vs. African-American names
    weat_dict['EuropeanAmerican_vs_AfricanAmerican_pleasant_vs_unpleasant'] = {
        'method': 'weat',
        'X_key': 'EuropeanAmerican',
        'Y_key': 'AfricanAmerican',
        'A_key': 'pleasant',
        'B_key': 'unpleasant',
        'targets': 'European-American names vs African-American names',
        'attributes': 'pleasant vs unpleasant',
    }
