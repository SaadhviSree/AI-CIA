import heapq

# 9. Branch and Bound with Estimate Heuristics
def branch_and_bound_cost_estimation(graph, start, goal, oracle_weight, heuristics):
    pq = [(0, start, [start])]  # Priority queue with tuples (current total cost, current node, path so far)
    explored_paths = []  # To store all paths explored
    oracle_path = None  # Store the redefined oracle path
    current_oracle_weight = oracle_weight  # Oracle weight that can be updated
    visited = set()  # Track visited nodes

    while pq:
        # Get the node with the smallest estimated total cost (cost + heuristic)
        cost, node, path = heapq.heappop(pq)

        # If the goal is reached, confirm the oracle
        if node == goal:
            if cost <= current_oracle_weight:
                current_oracle_weight = cost  # Update the oracle weight
                oracle_path = path  # Confirm the oracle path
                explored_paths.append((path, cost, 'oracle_confirmed'))
            continue

        # If the current path exceeds the oracle weight, terminate this path
        if cost >= current_oracle_weight:
            explored_paths.append((path, cost, 'exceeded_oracle'))
            continue

        # If the node is already visited, mark it as explored and skip
        if node in visited:
            explored_paths.append((path, cost, 'already_explored'))
            continue
        
        visited.add(node)

        # Explore neighbors and add to priority queue if valid (not revisiting nodes in the current path)
        neighbors = graph.get(node, [])
        if not neighbors:  # Dead end, no further neighbors
            explored_paths.append((path, cost, 'dead_end'))

        for neighbor, weight in neighbors:
            if neighbor not in path:
                # Calculate the actual cost to reach the neighbor
                new_cost = cost + weight

                # Estimate the total cost using the heuristic
                estimated_total_cost = new_cost + heuristics[neighbor]

                # If the estimated total cost exceeds the oracle, terminate this path
                if estimated_total_cost > current_oracle_weight:
                    explored_paths.append((path + [neighbor], estimated_total_cost, 'exceeded_oracle'))
                else:
                    heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))  # Push the actual cost (not estimated cost)

    return oracle_path, current_oracle_weight, explored_paths
