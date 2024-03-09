"""
generates a bipartite matching using a approach similar to the Hopcroft–Karp Algorithm

Args:
    verticesL (list): list of vertex names on the left side
    verticesR (list): list of vertex names on the right side
    edges (dict): dict with vertex names as keys and a list of vertices to which they are matched as values ((n:m)-mapping)

Returns:
    list: of tuples which are finally matched in a (1:1)-mapping
"""
def findMaximumBipartiteMatching(verticesL, verticesR, edges):
    #initialize nodes and edges
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
    #begin algorithm
    augmentingPath = checkForAugmentingPath(startNode, endNode, edges)
    while augmentingPath:
        #send flow along augmenting path and update edges
        fromNode = endNode
        while fromNode != startNode:
            toNode = augmentingPath.get(fromNode)
            edges[fromNode].append(toNode)
            edges[toNode].remove(fromNode)
            fromNode = toNode
        edges[startNode].append(fromNode)
        edges[fromNode].remove(startNode)
        #compute new augmenting path if one exists
        augmentingPath = checkForAugmentingPath(startNode, endNode, edges)
    #prepare bipartite matching
    matching = []
    for rightNode in edges[endNode]:
        leftNode = edges[rightNode][0]
        matching.append((leftNode, rightNode))
    return matching

#iterative BFS with queue stops if reached the node endNode
#returns a dict with nodes as keys and nodes form which they are reached as values
def checkForAugmentingPath(startNode, endNode, edges):
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