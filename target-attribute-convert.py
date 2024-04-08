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

    # Target - attribute pairings
    pairings = [
        ('flowers', 'insects', 'pleasant', 'unpleasant'),
        ('instruments', 'weapons', 'pleasant', 'unpleasant'),
        ('EuropeanAmerican names', 'AfricanAmerican names', 'pleasant', 'unpleasant'),
        ('male names', 'female names', 'career', 'family'),
        ('math', 'arts', 'male terms', 'female terms'),
        ('science', 'arts', 'male terms', 'female terms'),
        ('mental diseases', 'physical diseases', 'temporary', 'permanent'),
        ('young names', 'old names', 'pleasant', 'unpleasant')
    ]

    # Iterate over each pairing and populate the dictionary
    for x_key, y_key, a_key, b_key in pairings:
        # Standardize keys: remove underscores and convert to lowercase
        std_x_key = x_key.replace('_', '').lower()
        std_y_key = y_key.replace('_', '').lower()
        std_a_key = a_key.replace('_', '').lower()
        std_b_key = b_key.replace('_', '').lower()

        # Create dictionary structure for each pairing
        weat_dict[f'{std_x_key}_vs_{std_y_key}_and_{std_a_key}_vs_{std_b_key}'] = {
            'method': 'weat',
            'X_key': std_x_key,
            'Y_key': std_y_key,
            'A_key': std_a_key,
            'B_key': std_b_key,
            'targets': f'{std_x_key} vs {std_y_key}',
            'attributes': f'{std_a_key} vs {std_b_key}',
        }

    # Save to JSON file
    with open(output_path, 'w') as f:
        json.dump(weat_dict, f, sort_keys=True, indent=4)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weat_dir', type=str, required=True,
                        help='WEAT data directory containing word lists')
    parser.add_argument('--output', type=str, default='weat.json',
                        help='Output JSON file path')
    args = parser.parse_args()

    create_weat_dict(args.weat_dir, args.output)

if __name__ == '__main__':
    main()
