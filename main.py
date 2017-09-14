import ngrams
import phrasescoring
import sentencefinder

# this is just an example of all the different pieces working together

sample_phrases = [
    "Despite a",
    "recent downturn",
    "in",
    "sales",
    "in about a year",
    "our company",
    "will release a",
    "brand new feature",
    "which",
    "we",
    "expect to boost",
    "total revenue"
]

grams = ngrams.all_grams(sample_phrases, 4)
scored_grams = phrasescoring.score_grams(grams)
best_grams = sentencefinder.best_full_gram_subset(scored_grams)
print(best_grams)
