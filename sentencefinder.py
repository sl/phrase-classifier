# Construct a graph (in the form of an adjacency list) from a list
# of n-grams and their placement information.
def construct_graph_from_grams(grams):
  # 0 is the start in the adjacency list,
  # each index i after that maps to i + 1 in grams,
  # the last index in the adjacency list is the terminator
  # 
  # lineUp is used to make numbers match better between
  # grams and the adjacency list
  lineUp = [None] + grams

  adjList = [[] for i in range(len(grams) + 2)]

  highestEnd = -1
  endMap = {}
  endMap[-1] = [0]
  for i in range(1, len(lineUp)):
    (gram, indexes, score) = lineUp[i]

    if indexes[-1] > highestEnd:
      highestEnd = indexes[-1]

    if indexes[-1] in endMap:
      endMap[indexes[-1]].append(i)
    else:
      endMap[indexes[-1]] = [i]

  for i in range(1, len(lineUp)):
    (gram, indexes, score) = lineUp[i]

    for connection in endMap[indexes[0] - 1]:
      adjList[connection].append((i, score, lineUp[i]))

  for endConnection in endMap[highestEnd]:
    adjList[endConnection].append((len(lineUp), 0, None))

  return adjList











