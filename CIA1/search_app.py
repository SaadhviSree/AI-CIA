import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import tempfile
from British_Museum_Search import british_museum_search
from DFS import dfs
from BFS import bfs
from Hill_Climbing import hill_climbing
from Beam_Search import beam_search
from Oracle_Search import oracle_search
from BnB import branch_and_bound
from BnB_Extention import branch_and_bound_extended
from BnB_Est_Heuristics import branch_and_bound_cost_estimation
from Astar import a_star
from Best_First_Search import best_first_search

def run_oracle_if_needed(graph, start, goal, oracle_value):
    if not oracle_value:
        oracle_value = oracle_search(graph, start, goal)
    return oracle_value

@st.cache_data
def get_positions(graph):
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node]:
            G.add_edge(node, neighbor, weight=weight)
    pos = nx.spring_layout(G)
    return pos


def draw_graph(graph, pos, path=None):
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node]:
            G.add_edge(node, neighbor, weight=weight)

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='green', node_size=500)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name, bbox_inches='tight')  
    plt.close()  

    return temp_file.name 

def main():
    st.title("Search Algorithms Visualizer")

    graph_input = st.text_area("Graph Dictionary (Python dict)", placeholder="e.g., {'S': [('A', 3), ('B', 5)], ...}")

    if graph_input:
        graph = eval(graph_input)
        nodes = list(graph.keys())
        positions = get_positions(graph)

        st.write("Generated Graph:")
        fig, ax = plt.subplots(figsize=(4, 4))
        img_path = draw_graph(graph, positions)  # Draw graph and get image path
        st.image(img_path, use_column_width=False, width=400)
        st.markdown(
            """
            <style>
            .stImage {
                display: flex;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        algorithm = st.selectbox("Choose Algorithm", [
            "British Museum Search", "Depth First Search", "Breadth First Search", 
            "Hill Climbing Search", "Beam Search", "Oracle Search", 
            "Branch and Bound", "Branch and Bound with Extension List", 
            "Branch and Bound with Estimated Heuristics", "A*", "Best First Search"
        ])

        col1, col2 = st.columns(2)
        with col1: start_node = st.selectbox("Start Node", nodes)
        with col2: goal_node = st.selectbox("Goal Node", [node for node in nodes if node != start_node])

        heuristics = None
        oracle_value = None
        beam_width = None

        if algorithm == "Hill Climbing Search" or algorithm == "Beam Search" or algorithm in [
            "Branch and Bound with Estimated Heuristics", "A*", "Best First Search"]:
            heuristics_input = st.text_area("Heuristics Dictionary (Python dict)", placeholder="e.g., {'A': 1, 'B': 2, ...}")
            heuristics = eval(heuristics_input) if heuristics_input else None

        if algorithm == "Beam Search":
            beam_width = st.number_input("Beam Width", min_value=1, step=1)

        if algorithm in ["Branch and Bound", "Branch and Bound with Extension List", 
                         "Branch and Bound with Estimated Heuristics", "A*", "Best First Search"]:
            oracle_input = st.text_input("Oracle Value (optional)")
            oracle_value = int(oracle_input) if oracle_input else None

        if oracle_value is None and algorithm in ["Branch and Bound", "Branch and Bound with Extension List", 
                                                  "Branch and Bound with Estimated Heuristics", "A*"]:
            oracle_value = run_oracle_if_needed(graph, start_node, goal_node, oracle_value)

        if st.button("Run Algorithm"):
            try:
                if algorithm == "British Museum Search":
                    all_paths, paths_found = british_museum_search(graph, start_node, goal_node)
                elif algorithm == "Depth First Search":
                    path_found = dfs(graph, start_node, goal_node)[0]
                elif algorithm == "Breadth First Search":
                    path_found = bfs(graph, start_node, goal_node)[0]
                elif algorithm == "Hill Climbing Search":
                    path_found = hill_climbing(graph, start_node, goal_node, heuristics)
                elif algorithm == "Beam Search":
                    path_found, beams = beam_search(graph, start_node, goal_node, heuristics, beam_width)
                elif algorithm == "Oracle Search":
                    path_found, oracle_value, sub_opt_oracles = oracle_search(graph, start_node, goal_node)
                elif algorithm == "Branch and Bound":
                    path_found, oracle_value, all_paths = branch_and_bound(graph, start_node, goal_node, oracle_value)
                elif algorithm == "Branch and Bound with Extension List":
                    path_found, oracle_value, all_paths = branch_and_bound_extended(graph, start_node, goal_node, oracle_value)
                elif algorithm == "Branch and Bound with Estimated Heuristics":
                    path_found, oracle_value, all_paths = branch_and_bound_cost_estimation(graph, start_node, goal_node, oracle_value, heuristics)
                elif algorithm == "A*":
                    path_found, oracle_value, all_paths = a_star(graph, start_node, goal_node, oracle_value, heuristics)
                elif algorithm == "Best First Search":
                    path_found = best_first_search(graph, start_node, goal_node, heuristics)

                if algorithm == "British Museum Search":
                    st.write("Graph with Each Path Highlighted:")
                    for idx, path in enumerate(paths_found):
                        st.success(f"Path {idx + 1}: {path}")
                        fig, ax = plt.subplots(figsize=(4, 4))
                        img_path = draw_graph(graph, positions, path)  # Draw graph and get image path
                        st.image(img_path, use_column_width=False, width=400)
                        st.markdown(
                            """
                            <style>
                            .stImage {
                                display: flex;
                                justify-content: center;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                elif algorithm in ["Oracle Search", "Branch and Bound", "Branch and Bound with Extension List", "Branch and Bound with Estimated Heuristics", "A*"]:
                    st.write("Graph with Path Highlighted:")
                    st.success(f"Path Found: {path_found}")
                    st.success(f"Oracle Value : {oracle_value}")
                    fig, ax = plt.subplots(figsize=(4, 4))
                    img_path = draw_graph(graph, positions, path)  # Draw graph and get image path
                    st.image(img_path, use_column_width=False, width=400)
                    st.markdown(
                        """
                        <style>
                        .stImage {
                            display: flex;
                            justify-content: center;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.write("Graph with Path Highlighted:")
                    st.success(f"Path Found: {path_found}")
                    fig, ax = plt.subplots(figsize=(4, 4))
                    img_path = draw_graph(graph, positions, path)  # Draw graph and get image path
                    st.image(img_path, use_column_width=False, width=400)
                    st.markdown(
                        """
                        <style>
                        .stImage {
                            display: flex;
                            justify-content: center;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
