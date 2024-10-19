from collections import deque

# 3. Breadth First Search (BFS)
def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    encountered_order = []  # To store the order in which nodes are encountered
    goal_path = None  # To store the path when the goal is found

    while queue:
        level_size = len(queue)  # Track nodes at the current level
        current_level_nodes = []  # To store nodes at the current level

        for _ in range(level_size):
            node, path = queue.popleft()
            current_level_nodes.append(node)  # Add node to current level order

            # Add to encountered order when encountered for the first time
            if node not in encountered_order:  
                encountered_order.append(node)

            if node == goal and goal_path is None:
                goal_path = path  # Store the first path when goal is encountered

            # Get neighbors and sort them lexicographically
            neighbors = sorted(neighbor for neighbor, _ in graph.get(node, []) if neighbor not in path)
            # Append neighbors to queue in sorted order
            for neighbor in neighbors:
                queue.append((neighbor, path + [neighbor]))

        if goal_path is not None:  # If goal is found, break after the current level is processed
            break

    # Return the path if goal is found, otherwise None, along with the encountered order
    return goal_path, encountered_order if goal_path else (None, encountered_order)
