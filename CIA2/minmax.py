import math
def minimax(depth, nodeIndex, isMaximizingPlayer, values, maxDepth):
    #terminal node(leaf nodes)
    if depth == maxDepth:
        print(f"Leaf node reached at depth {depth}, returning value: {values[nodeIndex]}")
        return values[nodeIndex]

    if isMaximizingPlayer:
        best = -math.inf

        #print(f"Maximizer at depth {depth}, evaluating children of node {nodeIndex}")
        print(f"Maximizer at depth {depth}")
        #maximizer's choice (MAX player)
        for i in range(2):
            value = minimax(depth + 1, nodeIndex * 2 + i, False, values, maxDepth)
            print(f"Maximizer at depth {depth}, comparing value: {value} with best: {best}")
            best = max(best, value)
        print(f"Maximizer at depth {depth}, selected best: {best}")
        return best
    else:
        best = math.inf

        #print(f"Minimizer at depth {depth}, evaluating children of node {nodeIndex}")
        print(f"Minimizer at depth {depth}")
        #minimizer's choice (MIN player)
        for i in range(2):
            value = minimax(depth + 1, nodeIndex * 2 + i, True, values, maxDepth)
            print(f"Minimizer at depth {depth}, comparing value: {value} with best: {best}")
            best = min(best, value)
        print(f"Minimizer at depth {depth}, selected best: {best}")
        return best
