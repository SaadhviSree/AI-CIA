# 4. Hill Climbing Search
def hill_climbing(graph, start, goal, heuristics):
    def backtrack(path):
        # Helper function to backtrack when a dead end is reached.
        while path:
            current = path.pop()  # Backtrack to the previous node
            # Check if any unexplored neighbor has a better heuristic
            neighbors = sorted(graph.get(current, []), key=lambda x: heuristics.get(x[0], float('inf')))
            for neighbor, _ in neighbors:
                if neighbor not in path:  # Check for unexplored neighbors
                    path.append(current)  # Add the current node back to the path
                    return neighbor
        return None  # No valid backtracking option

    current = start
    path = [current]
    visited = set([current])

    while current != goal:
        # Get neighbors sorted by heuristic values
        neighbors = sorted(graph.get(current, []), key=lambda x: heuristics.get(x[0], float('inf')))
        next_node = None

        # Find the best next node with a lower heuristic, if any
        for neighbor, _ in neighbors:
            if neighbor not in visited:
                next_node = neighbor
                break

        # If no improvement is found or dead end is reached, backtrack
        if not next_node or heuristics[current] <= heuristics[next_node]:
            next_node = backtrack(path)
            if not next_node:  # No more nodes to explore, return failure
                return None
        current = next_node
        visited.add(current)
        path.append(current)

    return path if current == goal else None
