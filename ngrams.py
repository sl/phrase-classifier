# creates n grams from a list for all i in 1 <= i <= n
def all_grams(l, n):
  res = []
  for i in range(1, n + 1):
    res = res + ngrams(l, i)
  return res

# changes the format of an n-gram from (items..., [indices])
# to ([items], [indices])
def format_ngram(ngram):
  l = list(ngram)
  first = l[:-1]
  second = l[-1]
  return (first, second)

# creates n-grams from a list by rolling a slice over the list
# and zipping the results
def ngrams(l, n):
  ngrams = zip(*([l[x:] for x in range(n)] + [[list(range(i, i + n)) for i in range(len(l))]]))
  return map(format_ngram, ngrams)