# 5. Beam Search
def beam_search(graph, start, goal, heuristics, beam_width=2):
    queue = [(start, [start])]
    beams_per_level = []  # To track the beam chosen at each level
    
    while queue:
        # Sort the current queue based on heuristic values and choose the top 'beam_width' nodes
        queue = sorted(queue, key=lambda x: heuristics.get(x[0], float('inf')))[:beam_width]
        
        # Record the nodes at this level (beam)
        beams_per_level.append([node for node, _ in queue])
        
        next_queue = []
        for node, path in queue:
            if node == goal:
                return path, beams_per_level  # Return the path and the beam history
            
            # Explore neighbors and add to the next level queue if not already in the path
            for neighbor, _ in graph.get(node, []):
                if neighbor not in path:
                    next_queue.append((neighbor, path + [neighbor]))
        
        queue = next_queue
    
    return None, beams_per_level  # Return None if no path to goal is found, but still show beams
