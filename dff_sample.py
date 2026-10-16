
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# --------------------------------------------------
# 1. DEFAULT DIRECTED GRAPH
# --------------------------------------------------

DEFAULT_GRAPH = {
    "A": ["B", "D"],
    "B": ["C", "E", "G"],
    "C": ["A"],
    "D": ["C"],
    "E": ["H"],
    "F": [],
    "G": ["F"],
    "H": ["F", "G"]
}

DEFAULT_EDGE_TEXT = """A B
A D
B C
B E
B G
C A
D C
E H
G F
H F
H G"""


# --------------------------------------------------
# 2. GRAPH INPUT AND VALIDATION
# --------------------------------------------------

def read_graph(edge_text):
    """Convert text input into a directed adjacency list."""
    graph = {}

    for line_number, line in enumerate(edge_text.splitlines(), 1):
        line = line.split("#", 1)[0].strip()

        if not line:
            continue

        parts = line.replace(",", " ").upper().split()

        if len(parts) not in (1, 2):
            raise ValueError(
                f"Invalid input on line {line_number}: {line}"
            )

        source = parts[0]

        if not source.isalpha() or len(source) != 1:
            raise ValueError("Use single-letter node names, A to Z.")

        graph.setdefault(source, [])

        if len(parts) == 2:
            target = parts[1]

            if not target.isalpha() or len(target) != 1:
                raise ValueError(
                    "Use single-letter node names, A to Z."
                )

            graph[source].append(target)
            graph.setdefault(target, [])

    if not graph:
        raise ValueError("Please enter at least one node.")

    if len(graph) > 26:
        raise ValueError("A maximum of 26 nodes is allowed.")

    # Remove duplicate edges and sort neighbors alphabetically.
    for node in graph:
        graph[node] = sorted(set(graph[node]))

    return dict(sorted(graph.items()))


# --------------------------------------------------
# 3. BREADTH-FIRST SEARCH
# --------------------------------------------------

def bfs_search(graph, start, goal=None):
    """Explore nodes level by level using a FIFO queue."""

    queue = deque([start])
    discovered = {start}

    parent = {start: None}
    level = {start: 0}

    visited_order = []
    step_history = []

    while queue:
        current = queue.popleft()
        visited_order.append(current)

        # Stop expanding when the goal is reached.
        if current != goal:
            for neighbor in graph[current]:
                if neighbor not in discovered:
                    discovered.add(neighbor)
                    parent[neighbor] = current
                    level[neighbor] = level[current] + 1
                    queue.append(neighbor)

        step_history.append({
            "Step": len(step_history) + 1,
            "Current Node": current,
            "Level": level[current],
            "Parent": parent[current] or "-",
            "Visited Order": " -> ".join(visited_order),
            "Frontier Queue": " -> ".join(queue) or "Empty"
        })

        if current == goal:
            break

    return build_result(
        "BFS", start, goal, visited_order,
        parent, level, step_history
    )


# --------------------------------------------------
# 4. DEPTH-FIRST SEARCH
# --------------------------------------------------

def dfs_search(graph, start, goal=None):
    """Explore one branch deeply before backtracking."""

    visited = set()
    parent = {start: None}
    level = {start: 0}

    visited_order = []
    step_history = []
    active_path = []

    def visit(current):
        # Return if this node has already been visited.
        if current in visited:
            return False

        visited.add(current)
        visited_order.append(current)
        active_path.append(current)

        step_history.append({
            "Step": len(step_history) + 1,
            "Current Node": current,
            "Level": level[current],
            "Parent": parent[current] or "-",
            "Visited Order": " -> ".join(visited_order),
            "DFS Stack": " -> ".join(active_path)
        })

        # Goal test.
        if current == goal:
            return True

        # Neighbors are visited in alphabetical order.
        for neighbor in graph[current]:
            if neighbor not in visited:
                parent[neighbor] = current
                level[neighbor] = level[current] + 1

                if visit(neighbor):
                    return True

        active_path.pop()
        return False

    visit(start)

    return build_result(
        "DFS", start, goal, visited_order,
        parent, level, step_history
    )


# --------------------------------------------------
# 5. BUILD SEARCH RESULTS
# --------------------------------------------------

def build_result(method, start, goal, order,
                 parent, level, trace):

    found = goal is None or goal in order
    path = []

    if goal is not None and found:
        node = goal

        while node is not None:
            path.append(node)
            node = parent[node]

        path.reverse()

    return {
        "method": method,
        "order": order,
        "path": path,
        "found": found,
        "parent": parent,
        "level": level,
        "trace": trace,
        "expanded": len(order),
        "max_level": max(level.values(), default=0)
    }


# --------------------------------------------------
# 6. GRAPH VISUALIZATION
# --------------------------------------------------

def visualize_search(graph, result, step):
    """Display visited nodes and the current expansion."""

    network = nx.DiGraph()

    for node, neighbors in graph.items():
        network.add_node(node)

        for neighbor in neighbors:
            network.add_edge(node, neighbor)

    # Fixed layout keeps the display consistent.
    positions = {
        "A": (0, 2),
        "B": (1, 1),
        "C": (0, 0),
        "D": (-1, 1),
        "E": (2, 2),
        "H": (3, 2),
        "G": (2, 0),
        "F": (3, 0)
    }

    # Add a fallback position for custom nodes.
    for index, node in enumerate(network.nodes):
        if node not in positions:
            positions[node] = (index, -1)

    current = result["trace"][step - 1]["Current Node"]
    visited = set(
        result["order"][:step]
    )

    colors = []

    for node in network.nodes:
        if node == current:
            colors.append("#22c55e")
        elif node in visited:
            colors.append("#93c5fd")
        else:
            colors.append("#e5e7eb")

    fig, ax = plt.subplots(figsize=(8, 5))

    nx.draw_networkx(
        network,
        positions,
        ax=ax,
        with_labels=True,
        node_color=colors,
        node_size=1100,
        font_size=12,
        font_weight="bold",
        edge_color="#64748b",
        arrows=True,
        arrowsize=20,
        connectionstyle="arc3,rad=0.04"
    )

    ax.set_title(
        f"{result['method']} Search - Step {step}",
        fontsize=13
    )
    ax.axis("off")
    fig.tight_layout()

    return fig


# --------------------------------------------------
# 7. STREAMLIT PAGE
# --------------------------------------------------

st.set_page_config(
    page_title="BFS and DFS Search Visualizer",
    page_icon="🔎",
    layout="wide"
)

st.title("BFS and DFS Search Visualizer")

st.caption(
    "BSD3513 Artificial Intelligence | Lab Report 1"
)

with st.expander("How the algorithms work"):
    st.markdown("""
    - **BFS:** Uses a FIFO queue and explores nodes level by level.
    - **DFS:** Uses a recursive stack and explores a branch deeply
      before backtracking.
    - **Alphabetical tie-breaking:** Adjacent nodes are explored
      in alphabetical order.
    - **Level:** The number of edges from the starting node
      along the selected search tree.
    - **Parent:** The node from which a node was first discovered.
    """)

# --------------------------------------------------
# 8. SIDEBAR SETTINGS
# --------------------------------------------------

with st.sidebar:
    st.header("Search Settings")

    edge_text = st.text_area(
        "Directed edges",
        value=DEFAULT_EDGE_TEXT,
        height=260,
        help="Enter one directed edge per line, such as A B."
    )

    st.caption(
        "You may enter a single node on a line to represent "
        "an isolated node."
    )

    algorithm = st.selectbox(
        "Search algorithm",
        ["Both", "BFS", "DFS"]
    )

# --------------------------------------------------
# 9. VALIDATE GRAPH AND SELECT NODES
# --------------------------------------------------

try:
    graph = read_graph(edge_text)

except ValueError as error:
    st.error(str(error))
    st.stop()

nodes = list(graph.keys())

col1, col2 = st.columns(2)

with col1:
    start = st.selectbox(
        "Starting Node",
        nodes,
        index=nodes.index("A") if "A" in nodes else 0
    )

with col2:
    goal_options = ["No goal"] + nodes

    goal_selection = st.selectbox(
        "Goal Node (optional)",
        goal_options,
        index=0
    )

goal = (
    None if goal_selection == "No goal"
    else goal_selection
)

if goal is not None and goal == start:
    st.info("The start node is already the goal node.")

# --------------------------------------------------
# 10. EXECUTE SEARCH
# --------------------------------------------------

selected_algorithms = (
    ["BFS", "DFS"] if algorithm == "Both"
    else [algorithm]
)

results = {}

for method in selected_algorithms:
    if method == "BFS":
        results[method] = bfs_search(graph, start, goal)
    else:
        results[method] = dfs_search(graph, start, goal)

# --------------------------------------------------
# 11. DISPLAY SEARCH RESULTS
# --------------------------------------------------

for method, result in results.items():

    st.divider()
    st.header(f"{method} Search Results")

    st.write(
        "**Expansion Order:** "
        + " → ".join(result["order"])
    )

    if goal is not None:
        if result["found"]:
            st.write(
                "**Process Path to Goal:** "
                + " → ".join(result["path"])
            )
        else:
            st.warning(
                f"Goal {goal} is not reachable from {start}."
            )

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Expanded Nodes",
        result["expanded"]
    )

    metric2.metric(
        "Maximum Level",
        result["max_level"]
    )

    metric3.metric(
        "Path Length (Edges)",
        len(result["path"]) - 1
        if goal is not None and result["found"]
        else "N/A"
    )

    # Show every node's level and parent.
    st.subheader("Node Level and Parent Table")

    node_rows = []

    for node in result["order"]:
        node_rows.append({
            "Node": node,
            "Level": result["level"][node],
            "Parent": result["parent"][node] or "-",
            "Expansion Position":
                result["order"].index(node) + 1
        })

    st.dataframe(
        pd.DataFrame(node_rows),
        hide_index=True,
        use_container_width=True
    )

    # Step-by-step exploration.
    st.subheader("Step-by-Step Process")

    step = st.slider(
        f"Select {method} step",
        min_value=1,
        max_value=len(result["trace"]),
        value=len(result["trace"]),
        key=f"step_{method}"
    )

    left, right = st.columns([1.2, 1])

    with left:
        figure = visualize_search(graph, result, step)
        st.pyplot(figure)
        plt.close(figure)

    with right:
        st.dataframe(
            pd.DataFrame(result["trace"]),
            hide_index=True,
            use_container_width=True
        )

    current_trace = result["trace"][step - 1]

    st.info(
        f"Step {step}: Expanded node "
        f"{current_trace['Current Node']} "
        f"at Level {current_trace['Level']}."
    )

# --------------------------------------------------
# 12. BFS VS DFS COMPARISON
# --------------------------------------------------

if algorithm == "Both":

    st.divider()
    st.header("BFS vs DFS Comparison")

    bfs = results["BFS"]
    dfs = results["DFS"]

    comparison_rows = [
        {
            "Measure": "Data Structure",
            "BFS": "FIFO Queue",
            "DFS": "Recursive Stack"
        },
        {
            "Measure": "Expansion Order",
            "BFS": " → ".join(bfs["order"]),
            "DFS": " → ".join(dfs["order"])
        },
        {
            "Measure": "Expanded Nodes",
            "BFS": bfs["expanded"],
            "DFS": dfs["expanded"]
        },
        {
            "Measure": "Maximum Level",
            "BFS": bfs["max_level"],
            "DFS": dfs["max_level"]
        }
    ]

    if goal is not None:
        comparison_rows.extend([
            {
                "Measure": "Goal Path",
                "BFS": " → ".join(bfs["path"]) or "Not found",
                "DFS": " → ".join(dfs["path"]) or "Not found"
            },
            {
                "Measure": "Goal Path Length (Edges)",
                "BFS": len(bfs["path"]) - 1
                if bfs["found"] else "N/A",
                "DFS": len(dfs["path"]) - 1
                if dfs["found"] else "N/A"
            }
        ])

    st.dataframe(
        pd.DataFrame(comparison_rows),
        hide_index=True,
        use_container_width=True
    )

    st.markdown("""
    **Conclusion:** BFS explores nodes level by level and finds
    a minimum-edge path in an unweighted graph when a goal is
    reachable. DFS explores deeper branches before backtracking
    and does not guarantee a minimum-edge path.
    """)

# --------------------------------------------------
# 13. GRAPH SUMMARY
# --------------------------------------------------

st.divider()
st.subheader("Graph Information")

summary1, summary2, summary3 = st.columns(3)

summary1.metric("Total Nodes", len(graph))

summary2.metric(
    "Total Directed Edges",
    sum(len(neighbors) for neighbors in graph.values())
)

summary3.metric(
    "Starting Node",
    start
)

st.caption(
    "Developed for educational purposes. "
    "Verify the displayed graph against the assignment diagram."
)
