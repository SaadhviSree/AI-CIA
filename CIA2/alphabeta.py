import math

def minmax_alpha_beta(depth, nodeIndex, isMaximizingPlayer, values, maxDepth, alpha, beta, pruned_nodes):
    # Terminal node (leaf nodes)
    if depth == maxDepth:
        print(f"Leaf node reached at depth {depth}, returning value: {values[nodeIndex]}")
        return values[nodeIndex]

    if isMaximizingPlayer:
        best = -math.inf
        print(f"Maximizer at depth {depth}")

        # Maximizer's choice (MAX player)
        for i in range(2):
            value = minmax_alpha_beta(depth + 1, nodeIndex * 2 + i, False, values, maxDepth, alpha, beta, pruned_nodes)
            print(f"Maximizer at depth {depth}, comparing value: {value} with best: {best}")
            best = max(best, value)
            alpha = max(alpha, best)
            
            # Alpha-beta pruning
            if beta <= alpha:
                print(f"Pruning at Maximizer depth {depth}, alpha: {alpha}, beta: {beta}")
                pruned_nodes[0] += 1  # Increment pruned nodes counter
                break
                
        print(f"Maximizer at depth {depth}, selected best: {best}")
        return best
    else:
        best = math.inf
        print(f"Minimizer at depth {depth}")

        # Minimizer's choice (MIN player)
        for i in range(2):
            value = minmax_alpha_beta(depth + 1, nodeIndex * 2 + i, True, values, maxDepth, alpha, beta, pruned_nodes)
            print(f"Minimizer at depth {depth}, comparing value: {value} with best: {best}")
            best = min(best, value)
            beta = min(beta, best)

            # Alpha-beta pruning
            if beta <= alpha:
                print(f"Pruning at Minimizer depth {depth}, alpha: {alpha}, beta: {beta}")
                pruned_nodes[0] += 1  # Increment pruned nodes counter
                break
                
        print(f"Minimizer at depth {depth}, selected best: {best}")
        return best
