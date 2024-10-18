import heapq

# 11. Best First Search
def best_first_search(graph, start, goal, heuristic):
    # Priority queue to store (cost, current_node, path)
    pq = [(heuristic[start], start, [start])]  
    visited = set()  # To track visited nodes

    while pq:
        # Get the node with the lowest heuristic cost
        _, node, path = heapq.heappop(pq)

        # If the goal is reached, return the path
        if node == goal:
            return path

        # If the node has already been visited, skip it
        if node in visited:
            continue
        
        # Mark the current node as visited
        visited.add(node)

        # Explore neighbors
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                # Add the neighbor to the priority queue with its heuristic cost
                heapq.heappush(pq, (heuristic[neighbor], neighbor, path + [neighbor]))

    return None  # Return None if no path is found
