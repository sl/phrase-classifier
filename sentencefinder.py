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

    adj_list = [([], []) for i in range(len(grams) + 2)]

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
            adj_list[connection][0].append((i, score, line_up[i]))
            adj_list[i][1].append(connection)

    for endConnection in end_map[highest_end]:
        adj_list[endConnection][0].append((len(line_up), 0, None))
        adj_list[len(adj_list) - 1][1].append(endConnection)

    return adj_list


# Itterative implementation of DFS topological sort using negative numbers
# to represent post processing steps on the work stack.
def topological_sort(graph):
    stack = []
    ordered = []
    visited = [False] * len(graph)
    for i in range(0, len(graph)):
        if not visited[i]:
            visited[i] = True
            stack.append(i)
            while stack:
                v = stack.pop()
                if v >= 0:
                    stack.append(-v - 1)
                    for (connected, _, _) in graph[v][0]:
                        if not visited[connected]:
                            visited[connected] = True
                            stack.append(connected)
                else:
                    ordered.append(-v - 1)
    return list(reversed(ordered))


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
            ([(1, 2, ('a', [0], 2)), (4, 3, ('ab', [0, 1], 3))], []),
            ([(2, 2, ('b', [1], 2)), (5, 4, ('bc', [1, 2], 4))], [0]),
            ([(3, 1, ('c', [2], 1))], [1]),
            ([(6, 0, None)], [2, 4]),
            ([(3, 1, ('c', [2], 1))], [0]),
            ([(6, 0, None)], [1]),
            ([], [3, 5])
        ]
        self.assertEqual(expected, construct_graph_from_grams(test_grams))

    def test_topological_sort(self):
        graph = [
            ([(1, 2, ('a', [0], 2)), (4, 3, ('ab', [0, 1], 3))], []),
            ([(2, 2, ('b', [1], 2)), (5, 4, ('bc', [1, 2], 4))], [0]),
            ([(3, 1, ('c', [2], 1))], [1]),
            ([(6, 0, None)], [2, 4]),
            ([(3, 1, ('c', [2], 1))], [0]),
            ([(6, 0, None)], [1]),
            ([], [3, 5])
        ]
        expected = [0, 1, 2, 5, 4, 3, 6]
        self.assertEqual(expected, topological_sort(graph))


if __name__ == '__main__':
    unittest.main()
