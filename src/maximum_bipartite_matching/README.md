# generateMaximumBipartiteMatching.py
## How it Works
1. **Initialization**: Start with an initial matching (in this case empty) and directed edges. Connect a start node to all left nodes and all right nodes to an end node. 
2. **Augmenting Paths**:
   - While there exists an augmenting path (path between start and end node using current edges) in the graph:
     - Use a breadth-first search (BFS) to efficiently find augmenting paths.
     - Update the matching by flipping the edges along the augmenting path.
3. **Repeat**: Repeat the process of finding augmenting paths and updating the matching until no augmenting paths can be found.
4. **Result**: The obtained matching is a maximum cardinality (1:1)-matching in the bipartite graph.
