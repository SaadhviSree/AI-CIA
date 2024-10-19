from collections import deque

# 6. Oracle Search
def oracle_search(graph, start, goal):
    # Queue stores tuples of (current_node, path_taken, total_path_weight)
    queue = deque([(start, [start], 0)])  
    oracle_path = None
    oracle_weight = float('inf')  # Keep track of the minimum weight (oracle)
    suboracles = []  # To store all paths to the goal and their weights

    while queue:
        node, path, path_weight = queue.popleft()
        
        if node == goal:
            # When goal is reached, store the path and its total weight
            suboracles.append((path, path_weight))
            if path_weight < oracle_weight:
                oracle_path = path  # Update the oracle with the shortest weighted path
                oracle_weight = path_weight
        
        # Traverse neighbors and calculate their path weights
        for neighbor, weight in graph.get(node, []):
            if neighbor not in path:  # Ensure no cycles
                queue.append((neighbor, path + [neighbor], path_weight + weight))
    
    return oracle_path, oracle_weight, suboracles
