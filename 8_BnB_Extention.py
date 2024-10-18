import heapq

# 8. Branch and Bound with Extended List
def branch_and_bound_extended(graph, start, goal, oracle_weight):
    pq = [(0, start, [start])]  # Priority queue with tuples (current cost, current node, path so far)
    explored_paths = []  # To store all paths explored
    oracle_path = None  # Store the redefined oracle path
    current_oracle_weight = oracle_weight  # Oracle weight that can be updated
    extension_list = set()  # Extension list to keep track of expanded nodes

    while pq:
        cost, node, path = heapq.heappop(pq)

        # If the node is already in the extension list, mark the path as explored and skip
        if node in extension_list:
            explored_paths.append((path, cost, 'explored'))
            continue

        # Add the node to the extension list
        extension_list.add(node)

        # If the goal is reached, confirm the oracle
        if node == goal:
            if cost <= current_oracle_weight:
                current_oracle_weight = cost  # Update the oracle weight
                oracle_path = path  # Confirm the oracle path
                explored_paths.append((path, cost, 'oracle_confirmed'))
            continue

        # If the current path exceeds the oracle weight, terminate this path and record
        if cost >= current_oracle_weight:
            explored_paths.append((path, cost, 'exceeded_oracle'))
            continue

        # Explore neighbors, sort them lexicographically and add to priority queue if valid
        neighbors = sorted(graph.get(node, []), key=lambda x: x[0])  # Sort by node name lexicographically
        if not neighbors:  # Dead end, no further neighbors
            explored_paths.append((path, cost, 'dead_end'))
        for neighbor, weight in neighbors:
            if neighbor not in path:  # Avoid revisiting nodes already in the current path
                new_cost = cost + weight
                if new_cost > current_oracle_weight:
                    explored_paths.append((path + [neighbor], new_cost, 'exceeded_oracle'))
                else:
                    heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

    return oracle_path, current_oracle_weight, explored_paths
