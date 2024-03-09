# generateMaximumBipartiteMatching.py
## How it Works
1. **Initialization**: Start with an initial matching (in this case empty). Connect start node to all left nodes and the end node to all right nodes. 
2. **Augmenting Paths**:
   - While there exists an augmenting path (alternating path between unmatched and matched edges) in the graph:
     - Use a breadth-first search (BFS) to efficiently find augmenting paths.
     - Update the matching by flipping the edges along the augmenting path.
3. **Repeat**: Repeat the process of finding augmenting paths and updating the matching until no augmenting paths can be found.
4. **Result**: The obtained matching is a maximum cardinality matching in the bipartite graph.