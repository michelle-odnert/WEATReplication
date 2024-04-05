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
def load_vectors(word_list, model):
    vectors = [model[word] for word in word_list if word in model]
    return np.array(vectors)

# load in target-attribute pairings
with open('weat_dict.json', 'r') as f:
    pairings = json.load(f)

# intiialize results list
weat_results = []

# Iterate over pairings and to compute weat score
for pairing_name, pairing_info in pairings.items():
    X = load_vectors(pairing_info['X_key'].split(), model)
    Y = load_vectors(pairing_info['Y_key'].split(), model)
    A = load_vectors(pairing_info['A_key'].split(), model)
    B = load_vectors(pairing_info['B_key'].split(), model)

    d = weat_effect_size(X, Y, A, B)
    p = weat_p_value(X, Y, A, B)

    # add to results list
    weat_results.append({
        'Target Words': pairing_info['targets'],
        'Attribute Words': pairing_info['attributes'],
        'Number of Target Words (Nt)': len(X) + len(Y),
        'Number of Attribute Words (Na)': len(A) + len(B),
        'd (effect size)': d,
        'p-value': p
    })

# Convert results to a DataFrame and save or display
results_df = pd.DataFrame(weat_results)
results_df.to_csv('weat_results.csv', index=False)
print(results_df)
