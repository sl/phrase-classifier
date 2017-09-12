# Specification

This is the specification for the phrase sentiment classfication algorithm. This is still very much a work in progress, so feel free to add to it or change it as you see fit. Just be sure to PR any changes, and we'll take a look!

## Algorithm Description

R-CNN works by attempting to guess which "regions" contain the most information within the image. It then narrows those regions down by their relevance / likelyhood of containing something recognizable until it is left with only the windows deemed "most useful." Finally, it uses a standard image classification technique on those windows.

This phrase classifier intends to process text in a similar manner. It will first use the standard NLP technique of "chunking" to find the different phrase components of the text. It will then create n-grams of these prase chunks up to a specified size.

With these phrase n-grams, we'll then use a supervised learning based classifer (or possibly some other heuristic for scoring, tbg) to score each n-gram based on its usefullness. Finally, a dynamic programming algorithm will be used to determine the highest scoring sequence of n-grams that contains each word exactly once. This highest scoring selection of n-grams will be the chunks we use for sentiment analysis.

Finally, we run an existing sentiment analyser on the chosen set of n-grams.

## Example Workflow

This sentence is chosen for an example as it contains a variety of different sentiments that would be useful to separate from one another. Note that some of the outputs for "best phrases" are just my guesses as to what the algorithm would pick. This is just to show how the algorithm works, and is not what the algorithm would actually output.

    "Despite a recent downturn in sales, in about a year, our company will release a brand new feature which we expect to boost total revenue!"

#### Chunking

    "[DP Despite a] [NP recent downturn] [PP in] [NP sales] , [PP in about a year], [NP our company] [VP will release a] [NP brand new feature] [PP which] [NP we] [VP expect to boost] [NP total revenue] !"

### N-gram creation with n of 2 (2 is chosen for simplicity, likely would be larger)

    [("Despite a", [0]), ("recent downturn", [1]), ("in", [2]), ("sales", [3]),
     ("in about a year", [4]), ("our company", [5]), ("will release a", [6]),
     ("brand new feature", [7]), ("which", [8]), ("we", [9]),
     ("expect to boost", [10]), ("total revenue", [11]),
     ("Despite a recent downturn", [0, 1]), ("recent downturn in", [1, 2]),
     ("in sales", [2, 3]), ("sales in about a year", [3, 4]),
     ("in about a year our company", [4, 5]), ("our company will release a", [5, 6]),
     ("will release a brand new feature", [6, 7]), ("brand new feature which", [7, 8]),
     ("which we", [8, 9]), ("we expect to boost", [9, 10]), ("expect to boost total revenue", [10, 11])]

### N-gram scoring (these scores are a very rough guess)

    [("Despite a", [0], 0.05), ("recent downturn", [1], 0.1), ("in", [2], 0.01),
     ("sales", [3], 0.07), ("in about a year", [4], 0.2), ("our company", [5], 0.12),
     ("will release a", [6], 0.13), ("brand new feature", [7], 0.6), ("which", [8], 0.1),
     ("we", [9], 0.01), ("expect to boost", [10], 0.68), ("total revenue", [11], 0.3),
     ("Despite a recent downturn", [0, 1], 0.83), ("recent downturn in", [1, 2], 0.3),
     ("in sales", [2, 3], 0.1), ("sales in about a year", [3, 4], 0.4),
     ("in about a year our company", [4, 5], 0.4), ("our company will release a", [5, 6], 0.3),
     ("will release a brand new feature", [6, 7], 0.81), ("brand new feature which", [7, 8], 0.5),
     ("which we", [8, 9], 0.3), ("we expect to boost", [9, 10], 0.62),
     ("expect to boost total revenue", [10, 11], 0.79)]

### Highest Value Full sentence Selection (agian, just a guess)

    [("Despite a recent downturn", [0, 1], 0.83), ("in sales", [2, 3], 0.1),
     ("in about a year our company", [4, 5], 0.4), ("will release a brand new feature", [6, 7], 0.81),
     ("which we", [8, 9], 0.3), ("expect to boost total revenue", [10, 11], 0.79)]

### Sentiment analysis (again, just a guess)

    [("Despite a recent downturn", ("Negative", 0.11)), ("in sales", ("Neutral, 0.5)),
     ("in about a year our company", ("Positive", 0.76)),
     ("will release a brand new feature", ("Positive", 0.54)), ("which we", ("Neutral", 0.41)),
     ("expect to boost total revenue", ("Positive", 89.23))]



