import random


# scores all the phrases in the set of two-tuple grams, and attaches
# the scores as the last element of a three-tuple
def score_grams(grams):
    return [attach_score(gram) for gram in grams]


# attaches a score to a two-tuple gram as the last element of a three-tuple
def attach_score(gram):
    (phrase, indexes) = gram
    score = score_phrase(phrase)
    return (phrase, indexes, score)


# score an array of words on how relavant it is
def score_phrase(phrase):
    return random.uniform(0, 1/3) * len(phrase)

# no unit tests necessary until this actually does something
