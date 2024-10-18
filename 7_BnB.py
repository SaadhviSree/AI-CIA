import heapq

# 7. Branch and Bound Search
def branch_and_bound(graph, start, goal, oracle_weight):
    pq = [(0, start, [start])]  # Priority queue with tuples (current cost, current node, path so far)
    explored_paths = []  # To store all paths explored
    oracle_path = None  # Store the redefined oracle path
    current_oracle_weight = oracle_weight  # Oracle weight that can be updated

    while pq:
        cost, node, path = heapq.heappop(pq)

        # If the goal is reached, confirm the oracle
        if node == goal:
            if cost <= current_oracle_weight:
                current_oracle_weight = cost  # Update the oracle weight
                oracle_path = path  # Confirm the oracle path
                explored_paths.append((path, cost, 'oracle_confirmed'))
            continue

        # If the current path exceeds the oracle weight, terminate this path and return the portion covered
        if cost >= current_oracle_weight:
            explored_paths.append((path, cost, 'exceeded_oracle'))
            continue


        # Explore neighbors and add to priority queue if valid (not revisiting nodes in the current path)
        neighbors = graph.get(node, [])
        if not neighbors:  # Dead end, no further neighbors
            explored_paths.append((path, cost, 'dead_end'))
        for neighbor, weight in neighbors:
            if neighbor not in path:
                new_cost = cost + weight
                # If the new cost exceeds the oracle, record and terminate the exploration of that path immediately
                if new_cost > current_oracle_weight:
                    explored_paths.append((path + [neighbor], new_cost, 'exceeded_oracle'))
                else:
                    heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

    return oracle_path, current_oracle_weight, explored_paths