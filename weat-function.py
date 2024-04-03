import numpy as np
from itertools import permutations
import random

# return unit vector
def unit_vector(v):
    return v/np.linalg.norm(v)

# return cosine between two vectors
def cos(v1, v2):
    v1u = unit_vector(v1)
    v2u = unit_vector(v2)
    # compute dot prodcut, ensure no floating-point errors
    return np.clip(np.dot(v1u, v2u), -1.0, 1.0)

# returns the association of word w with attribute words s(w, A, B)
# W: set of target word vectors
# w: a single word vector from the set, each will have an association score
# A: set 1 of attribute words' vector
# B: set 2 of attribute words' vector
def target_attribute_association(W, A, B):
    # iterate over each word vector a in A and b in B and w in W
    association_scores = np.array([np.mean([cos(w, a) for a in A]) - np.mean([cos(w, b) for b in B]) for w in W])
    return association_scores

# return the differential assocaition of the two sets of target words with the attribute
# X: set 1 of target words' vector
# Y: set 2 of target words' vector
# each of X and Y will be passed into W in target_attribute_associations
# A: set 1 of attribute words' vector
# B: set 2 of attribute words' vector
def t_a_differential_association(X, Y, A, B):
    return np.sum([target_attribute_association(x, A, B) for x in X]) - np.sum([target_attribute_association(y, A, B) for y in Y])

# return effect size (test statistic) - normalized measure of how seperated the associations between target and attribute are
# X: set 1 of target words' vector
# Y: set 2 of target words' vector
# A: set 1 of attribute words' vector
# B: set 2 of attribute words' vector
def weat_effect_size(X, Y, A, B):
    x_associations = np.array([target_attribute_association(x, A, B) for x in X])
    y_associations = np.array([target_attribute_association(y, A, B) for y in Y])
    return (np.mean(x_associations) - np.mean(y_associations)) / np.std(np.concatenate((x_associations, y_associations)))

# return one-sided p value using permutations (doesn't assume distribution of t-statistic)
# Permutation process: combine two sets of target words, generate permutations of combined set
    # for each permutation caclulate differential association score
    # count num times permutated stats are greater than or equal to observed statistic
    # small p value indivates observed differential assocaition is significantly greater than would be expected by chance
def weat_p_value(X, Y, A, B, permutations=10000):
    observed = t_a_differential_association(X, Y, A, B)
    combined_target_set = X + Y 
    count_perm_greater_observed = 0

    for _ in range(permutations):
        random.shuffle(combined_target_set)
        rand_X = combined_target_set[:len(X)]
        rand_Y = combined_target_set[len(X):]
        if t_a_differential_association(rand_X, rand_Y, A, B) > observed:
            count_perm_greater_observed += 1

    return count_perm_greater_observed / permutations