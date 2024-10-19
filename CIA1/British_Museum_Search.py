# 1. British Museum Search (Brute Force Search)
def british_museum_search(graph, start, goal):
    def dfs_all_paths(node, path):
        path.append(node)

        # Check if node has no unexplored neighbors (dead-end) or if goal is reached
        neighbors = sorted([neighbor for neighbor, _ in graph.get(node, []) if neighbor not in path])
        
        if node == goal:
            valid_paths.append(list(path))  # Add to valid paths if goal is reached
        if not neighbors:  # It's a dead-end if no unexplored neighbors
            all_paths.append(list(path))  # Add every dead-end or complete path
        else:
            for neighbor in neighbors:
                dfs_all_paths(neighbor, path)

        path.pop()  # Backtrack after exploring all neighbors

    all_paths = []  # Stores dead-end paths and complete paths
    valid_paths = []  # Stores only valid paths that reach the goal
    dfs_all_paths(start, [])
    return all_paths, valid_paths
