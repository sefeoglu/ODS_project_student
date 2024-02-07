#similar to Hopcroft–Karp Algorithm
def findMaximumBipartiteMatching(verticesL, verticesR, edges):
    startNode = 'startNode'
    endNode = 'endNode'
    edges[startNode] = []
    edges[endNode] = []
    for node in verticesL + verticesR:
        if not edges.get(node): 
            edges[node] = []
    for leftNode in verticesL:
        edges[startNode].append(leftNode)
    for rightNode in verticesR:
        edges[rightNode].append(endNode)
    augmentingPath = checkForAugmentingPath(startNode, endNode, edges)
    while augmentingPath:
        #send flow
        fromNode = endNode
        while fromNode != startNode:
            toNode = augmentingPath.get(fromNode)
            edges[fromNode].append(toNode)
            edges[toNode].remove(fromNode)
            fromNode = toNode
        edges[startNode].append(fromNode)
        edges[fromNode].remove(startNode)
        #update path
        augmentingPath = checkForAugmentingPath(startNode, endNode, edges)
    #prepare bipartite matching
    matching = []
    for rightNode in edges[endNode]:
        leftNode = edges[rightNode][0]
        matching.append((leftNode, rightNode))
    return matching

def checkForAugmentingPath(startNode, endNode, edges):
    #bfs
    Queue = [startNode]
    visitedFrom = {}
    while len(Queue) > 0:
        currentNode = Queue.pop(0)
        for node in edges.get(currentNode):
            if not visitedFrom.get(node):
                visitedFrom[node] = currentNode
                Queue.append(node)
                if node == endNode:
                    return visitedFrom
    return None

# verticesL = [1, 2, 3, 4, 5, 6]
# verticesR = ['A', 'B', 'C', 'D', 'E', 'F']
# edges = {1: ['A', 'B'], 2: ['B', 'C'], 3: ['C', 'D'], 4: ['E'], 5: ['F'], 6: ['F']}
# print(findMaximumBipartiteMatching(verticesL, verticesR, edges))