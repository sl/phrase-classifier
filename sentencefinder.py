import unittest


# Construct a graph (in the form of an adjacency list) from a list
# of n-grams and their placement information.
def construct_graph_from_grams(grams):
    # 0 is the start in the adjacency list,
    # each index i after that maps to i + 1 in grams,
    # the last index in the adjacency list is the terminator
    #
    # lineUp is used to make numbers match better between
    # grams and the adjacency list
    line_up = [None] + grams

    adj_list = [[] for i in range(len(grams) + 2)]

    highest_end = -1
    end_map = {}
    end_map[-1] = [0]
    for i in range(1, len(line_up)):
        (gram, indexes, score) = line_up[i]

        if indexes[-1] > highest_end:
            highest_end = indexes[-1]

        if indexes[-1] in end_map:
            end_map[indexes[-1]].append(i)
        else:
            end_map[indexes[-1]] = [i]

    for i in range(1, len(line_up)):
        (gram, indexes, score) = line_up[i]

        for connection in end_map[indexes[0] - 1]:
            adj_list[connection].append((i, score, line_up[i]))

    for endConnection in end_map[highest_end]:
        adj_list[endConnection].append((len(line_up), 0, None))

    return adj_list


class TestConstructGraphFromNGrams(unittest.TestCase):

    def test_sample(self):
        test_grams = [
            ('a', [0], 2),
            ('b', [1], 2),
            ('c', [2], 1),
            ('ab', [0, 1], 3),
            ('bc', [1, 2], 4)
        ]

        expected = [
            [(1, 2, ('a', [0], 2)), (4, 3, ('ab', [0, 1], 3))],
            [(2, 2, ('b', [1], 2)), (5, 4, ('bc', [1, 2], 4))],
            [(3, 1, ('c', [2], 1))],
            [(6, 0, None)],
            [(3, 1, ('c', [2], 1))],
            [(6, 0, None)],
            []
        ]
        self.failUnlessEqual(expected, construct_graph_from_grams(test_grams))


if __name__ == '__main__':
    unittest.main()
