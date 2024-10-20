import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import math

def minmax(depth, nodeIndex, isMaximizingPlayer, values, maxDepth):
    if depth == maxDepth:
        return values[nodeIndex]
    
    children = [nodeIndex * 2 + 1, nodeIndex * 2 + 2]
    if isMaximizingPlayer:
        best = -math.inf
        for child in children:
            if child < len(values):
                value = minmax(depth + 1, child, False, values, maxDepth)
                best = max(best, value)
        return best
    else:
        best = math.inf
        for child in children:
            if child < len(values):
                value = minmax(depth + 1, child, True, values, maxDepth)
                best = min(best, value)
        return best

def create_tree(depth):
    G = nx.balanced_tree(2, depth)
    return G

def assign_values_to_leaves(G, values):
    leaves = [n for n in G.nodes() if G.degree(n)==1 and n != 0]
    for i, leaf in enumerate(leaves):
        G.nodes[leaf]['value'] = values[i] if i < len(values) else 0
        G.nodes[leaf]['show_value'] = True  # Always show leaf values
    return G

def calculate_minmax_values(G, depth, is_maximizing):
    for level in range(depth-1, -1, -1):
        nodes_at_level = [n for n in G.nodes() if G.nodes[n]['layer'] == level]
        for node in nodes_at_level:
            children = [c for c in G.neighbors(node) if G.nodes[c]['layer'] > level]
            if children:
                if (level % 2 == 0) == is_maximizing:  # Max level
                    G.nodes[node]['value'] = max(G.nodes[child]['value'] for child in children)
                    G.nodes[node]['best_child'] = max(children, key=lambda c: G.nodes[c]['value'])
                else:  # Min level
                    G.nodes[node]['value'] = min(G.nodes[child]['value'] for child in children)
                    G.nodes[node]['best_child'] = min(children, key=lambda c: G.nodes[c]['value'])
                G.nodes[node]['show_value'] = False  # Initially hide non-leaf values
    return G

def draw_tree(G, step=None, show_all_values=False, highlight_path=None):
    fig, ax = plt.subplots(figsize=(10, 7))
    
    pos = {node: (G.nodes[node]['x'], -G.nodes[node]['layer']) for node in G.nodes()}
    
    nx.draw_networkx_edges(G, pos, ax=ax)
    
    node_colors = ['lightblue' for _ in G.nodes()]
    label_colours = {}

    if step is not None:
        for node, data in step['highlight'].items():
            node_colors[node] = data['color']
            if data['color'] == 'green':
                G.nodes[node]['show_value'] = True  # Show value for green nodes
    
    if highlight_path:
        for node in highlight_path:
            node_colors[node] = 'black'
            label_colours[node] = 'white'
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, ax=ax)
    
    labels = {}
    for node, data in G.nodes(data=True):
        if 'value' in data and (show_all_values or data.get('show_value', False)):
            labels[node] = f"{data['value']}"
        else:
            labels[node] = ""
    
    text_color = {node: label_colours.get(node, 'black') for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_color=text_color, ax=ax)
    
    plt.title("Minimax Algorithm Visualization")
    plt.axis('off')
    return fig

def generate_steps(G, depth):
    steps = []
    for level in range(depth-1, -1, -1):
        nodes_at_level = [n for n in G.nodes() if G.nodes[n]['layer'] == level]
        for node in nodes_at_level:
            children = [c for c in G.neighbors(node) if G.nodes[c]['layer'] > level]
            highlight = {node: {'color': 'green'}}
            for child in children:
                highlight[child] = {'color': 'red'}
            steps.append({'highlight': highlight})
    return steps

def assign_x_coordinates(G, node, x, layer_width):
    G.nodes[node]['x'] = x
    children = [c for c in G.neighbors(node) if G.nodes[c]['layer'] > G.nodes[node]['layer']]
    if children:
        left_x = x - layer_width / 4
        right_x = x + layer_width / 4
        assign_x_coordinates(G, children[0], left_x, layer_width / 2)
        assign_x_coordinates(G, children[1], right_x, layer_width / 2)

def get_optimal_path(G):
    path = [0]  # Start with the root node
    current_node = 0
    while 'best_child' in G.nodes[current_node]:
        current_node = G.nodes[current_node]['best_child']
        path.append(current_node)
    return path

st.title('Minimax Algorithm Visualizer')

st.write("""
This app visualizes the Minimax algorithm on a binary tree.
1. Use the slider to select the depth of the tree.
2. Enter comma-separated values for the leaf nodes.
3. Choose whether the root player is maximizing or minimizing.
4. Click 'Run Minimax' to see the algorithm in action.
5. The final tree shows the optimal path.
""")

depth = st.slider('Select tree depth', 1, 5, 2)
values_input = st.text_input('Enter leaf node values (comma-separated)')
is_maximizing = st.radio("Select the root player's strategy", ('Maximizing', 'Minimizing')) == 'Maximizing'

if st.button('Run Minimax'):
    values = [int(x.strip()) for x in values_input.split(',')]
    
    G = create_tree(depth)
    
    for node in G.nodes():
        G.nodes[node]['layer'] = nx.shortest_path_length(G, 0, node)
    
    assign_x_coordinates(G, 0, 0, 1)
    
    G = assign_values_to_leaves(G, values)
    
    # Use the minmax function to calculate the root value
    root_value = minmax(0, 0, is_maximizing, values, depth)
    
    # Calculate values for all nodes using the graph-based approach
    G = calculate_minmax_values(G, depth, is_maximizing)

    steps = generate_steps(G, depth)
    
    st.write("Initial Tree")
    fig = draw_tree(G)
    st.pyplot(fig)
    
    for i, step in enumerate(steps):
        st.write(f"Step {i+1}")
        fig = draw_tree(G, step)
        st.pyplot(fig)
    
    st.write("Final Tree (with optimal path highlighted)")
    optimal_path = get_optimal_path(G)
    fig = draw_tree(G, show_all_values=True, highlight_path=optimal_path)
    st.pyplot(fig)

    st.write(f"The {'maximum' if is_maximizing else 'minimum'} value at the root is: {G.nodes[0]['value']}")
