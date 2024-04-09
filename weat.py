import os
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors
import numpy as np
import json
import pandas as pd
from weat_function import unit_vector, cos, target_attribute_association, t_a_differential_association, weat_effect_size, weat_p_value


glove_input_file = 'GloVe/glove.6B.50d.txt'
word2vec_output_file = 'glove.6B.50d.txt.word2vec'
# convert to word2vec format
glove2word2vec(glove_input_file, word2vec_output_file)

# load GloVe model
model = KeyedVectors.load_word2vec_format('glove.6B.50d.txt.word2vec', binary=False)

# load words from each word list file
# find their corresponding vectors from GloVe model
def load_vectors(key, model, weat_dir='wordlists'):
    filename = f"{key.replace(' ', '_').lower()}"
    filepath = os.path.join(weat_dir, filename)
    
    word_list = []
    
    try:
        with open(filepath, 'r') as file:
            # Load each word, delete whitespace and convert to lower 
            word_list = [line.strip().lower() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return np.array([])

    # load the vectors for each word if exists in model
    vectors = np.array([model[word] for word in word_list if word in model])

    # debug if words were properly loaded
    print(f"Loaded {len(vectors)} vectors for {len(word_list)} words from {filename}")
    
    return vectors

# load in target-attribute pairings
with open('weat_dict.json', 'r') as f:
    pairings = json.load(f)

# intiialize results list
weat_results = []
weat_dir = 'wordlists' 

# Iterate over pairings to compute WEAT scores
for pairing_name, pairing_info in pairings.items():
    print(f"Processing {pairing_name}...")
    X = load_vectors(pairing_info['X_key'], model, weat_dir)
    print(f"Loaded X: {len(X)} vectors.")
    Y = load_vectors(pairing_info['Y_key'], model, weat_dir)
    print(f"Loaded Y: {len(Y)} vectors.")
    A = load_vectors(pairing_info['A_key'], model, weat_dir)
    print(f"Loaded A: {len(A)} vectors.")
    B = load_vectors(pairing_info['B_key'], model, weat_dir)
    print(f"Loaded B: {len(B)} vectors.")

    # Check for empty vector sets and skip the calculation if any set is empty
    if len(X) == 0 or len(Y) == 0 or len(A) == 0 or len(B) == 0:
        print(f"Skipping {pairing_name} due to missing data.")
        continue

    # Calculate WEAT effect size and p-value
    print("Calculating effect size and p-value...")
    d = weat_effect_size(X, Y, A, B)
    p = weat_p_value(X, Y, A, B)
    print(f"Calculated d: {d}, p: {p}")

    # Append results
    weat_results.append({
        'Target Words': pairing_info['targets'],
        'Attribute Words': pairing_info['attributes'],
        'Number of Target Words (Nt)': len(X) + len(Y),
        'Number of Attribute Words (Na)': len(A) + len(B),
        'd (effect size)': d,
        'p-value': p
    })
    print("Results appended.")

# Convert results to a DataFrame and save or display
results_df = pd.DataFrame(weat_results)
results_df.to_csv('weat_results.csv', index=False)
print(results_df)