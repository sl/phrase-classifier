import unittest


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
    indices = [l[x:] for x in range(n)]
    ngrams = zip(*(indices + [[list(range(i, i + n)) for i in range(len(l))]]))
    return list(map(format_ngram, ngrams))


class TestNGrams(unittest.TestCase):

    def test_format_ngram(self):
        test_gram = ('a', 'b', 'c', 'd', [1, 2, 3])
        expected = (['a', 'b', 'c', 'd'], [1, 2, 3])
        self.assertEqual(expected, format_ngram(test_gram))

    def test_ngrams(self):
        test_list = ['a', 'b', 'c', 'd', 'e']
        expected = [
            (['a', 'b', 'c'], [0, 1, 2]),
            (['b', 'c', 'd'], [1, 2, 3]),
            (['c', 'd', 'e'], [2, 3, 4])
        ]
        self.assertEqual(expected, ngrams(test_list, 3))

    def test_all_grams(self):
        test_list = ['a', 'b', 'c']
        expected = [
            (['a'], [0]),
            (['b'], [1]),
            (['c'], [2]),
            (['a', 'b'], [0, 1]),
            (['b', 'c'], [1, 2])
        ]
        self.assertEqual(expected, all_grams(test_list, 2))


if __name__ == '__main__':
    unittest.main()
