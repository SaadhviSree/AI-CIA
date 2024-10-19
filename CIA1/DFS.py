# 2. Depth First Search (DFS)
def dfs(graph, start, goal):
    stack = [(start, [start])]
    encountered_order = []  # To store the order in which nodes are encountered

    while stack:
        node, path = stack.pop()
        
        # Add to encountered order when encountered for the first time
        if node not in encountered_order:  
            encountered_order.append(node)

        if node == goal:
            return path, encountered_order
        
        # Get neighbors and sort them lexicographically
        neighbors = sorted(neighbor for neighbor, _ in graph.get(node, []) if neighbor not in path)
        # Push neighbors to stack in sorted order
        for neighbor in reversed(neighbors):  # Reverse to maintain order since stack pops last added first
            stack.append((neighbor, path + [neighbor]))

    return None, encountered_order  # In case no path is found
