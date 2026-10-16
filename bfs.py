
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time
from collections import deque

# ==================================================
# 1. GRAPH CONFIGURATION
# ==================================================

GRAPH_DATA = {
    'A': ['B', 'D'],
    'B': ['C', 'E', 'G'],
    'C': ['A'],
    'D': ['C'],
    'E': ['H'],
    'F': [],
    'G': ['F'],
    'H': ['F', 'G']
}
# ==================================================
# 2. GRAPH PREPARATION
# ==================================================
def prepare_graph(data):
    """Standardise node labels and sort adjacent nodes."""
    cleaned = {}

    for node, adjacent in data.items():
        node = str(node).strip().upper()
        cleaned[node] = sorted(
            set(str(n).strip().upper() for n in adjacent)
        )
    for adjacent in list(cleaned.values()):
        for node in adjacent:
            cleaned.setdefault(node, [])
    return dict(sorted(cleaned.items()))

def parse_edges(text):
    """Build a directed graph from the text editor."""
    network = {}
    for line in text.splitlines():
        line = line.split('#')[0].strip().replace(',', ' ')
        if not line:
            continue
        items = line.upper().split()
        if len(items) not in (1, 2):
            raise ValueError(f"Invalid edge entry: {line}")
        source = items[0]
        network.setdefault(source, [])
        if len(items) == 2:
            target = items[1]
            network[source].append(target)
            network.setdefault(target, [])

    if not network:
        raise ValueError("Please provide at least one node.")
    if len(network) > 100:
        raise ValueError("The graph cannot exceed 100 nodes.")
    return prepare_graph(network)

DEFAULT_TEXT = "\n".join(
    f"{source} {target}"
    for source, adjacent in GRAPH_DATA.items()
    for target in adjacent
) + "\nF"

# ==================================================
# 3. SEARCH ENGINE
# ==================================================
def run_search(network, source, destination=None, algorithm="BFS"):
    """Run BFS or DFS and record the search process."""

    network = prepare_graph(network)
    source = source.strip().upper()
    destination = destination.strip().upper() if destination else None
    if source not in network or (
        destination is not None and destination not in network
    ):
        raise ValueError("Starting node or goal node does not exist.")
    if algorithm not in ("BFS", "DFS"):
        raise ValueError("Choose BFS or DFS.")
    # Queue for BFS; stack for DFS.
    pending = deque([source]) if algorithm == "BFS" else [source]
    discovered = {source} if algorithm == "BFS" else set()
    parent_node = {source: None}
    node_level = {source: 0}
    expansion_order = []
    process_log = []
    while pending:
        current = (
            pending.popleft()
            if algorithm == "BFS"
            else pending.pop()
        )
        # Preserve the original DFS duplicate-entry behaviour.
        if algorithm == "DFS":
            if current in discovered:
                process_log.append({
                    "Step": len(process_log) + 1,
                    "Current Node": f"{current} (skip)",
                    "Visited": expansion_order.copy(),
                    "Frontier": list(pending),
                    "Level": node_level[current],
                    "Parent": parent_node[current]
                })
                continue
            discovered.add(current)
        expansion_order.append(current)
        if current != destination:
            adjacent_nodes = (
                network[current]
                if algorithm == "BFS"
                else list(reversed(network[current]))
            )
            for neighbor in adjacent_nodes:
                if neighbor not in discovered:
                    if algorithm == "BFS":
                        discovered.add(neighbor)
                    parent_node[neighbor] = current
                    node_level[neighbor] = node_level[current] + 1
                    pending.append(neighbor)
        process_log.append({
            "Step": len(process_log) + 1,
            "Current Node": current,
            "Visited": expansion_order.copy(),
            "Frontier": list(pending),
            "Level": node_level[current],
            "Parent": parent_node[current]
        })
        if current == destination:
            break
    # Reconstruct the path to the selected goal.
    route = []
    if destination is not None and destination in expansion_order:
        current = destination
        while current is not None:
            route.append(current)
            current = parent_node[current]
        route.reverse()
    return {
        "algorithm": algorithm,
        "order": expansion_order,
        "route": route,
        "found": bool(route) if destination else None,
        "trace": process_log,
        "levels": {
            node: node_level[node] for node in expansion_order
        },
        "parents": {
            node: parent_node[node] for node in expansion_order
        },
        "total_expanded": len(expansion_order),
        "largest_frontier": max(
            [1] + [len(item["Frontier"]) for item in process_log]
        )
    }
# ==================================================
# 4. GRAPH DRAWING
# ==================================================
def render_network(network, result, selected_step):
    """Highlight the current node and previously visited nodes."""
    diagram = nx.DiGraph()
    for node, adjacent in network.items():
        diagram.add_node(node)
        for neighbor in adjacent:
            diagram.add_edge(node, neighbor)
    figure, axis = plt.subplots(figsize=(7, 4.5))
    layout = nx.spring_layout(diagram, seed=13)
    current_record = result["trace"][selected_step - 1]
    current_node = current_record["Current Node"]
    visited_nodes = current_record["Visited"]
    node_colours = []
    for node in diagram.nodes:
        if node == current_node:
            node_colours.append("#10b981")
        elif node in visited_nodes:
            node_colours.append("#93c5fd")
        else:
            node_colours.append("#e5e7eb")

    nx.draw_networkx(
        diagram,
        layout,
        ax=axis,
        with_labels=True,
        node_color=node_colours,
        node_size=950,
        font_weight="bold",
        arrows=True,
        arrowsize=19,
        edge_color="#64748b"
    )

    axis.set_title(f"{result['algorithm']} - Search Step {selected_step}")
    axis.axis("off")

    return figure
# ==================================================
# 5. APPLICATION SETTINGS
# ==================================================
st.set_page_config(
    page_title="AI Search Lab",
    page_icon="🔎",
    layout="wide"
)
st.title("Interactive Graph Search")
st.caption(
    "BSD3513 Artificial Intelligence | Lab Report 1 | UMPSA"
)
with st.expander("Algorithm guide"):
    st.markdown("""
    **Breadth-First Search (BFS)** uses a FIFO queue to explore
    nodes level by level.
    **Depth-First Search (DFS)** uses a LIFO stack to explore a
    branch deeply before exploring alternatives.
    Both algorithms have O(V + E) time complexity with a standard
    adjacency-list implementation. BFS finds a shortest path in
    an unweighted graph; DFS does not guarantee one.
    """)
# ==================================================
# 6. SIDEBAR CONTROLS
# ==================================================
with st.sidebar:
    st.header("Graph Controls")
    edge_input = st.text_area(
        "Directed connections",
        value=DEFAULT_TEXT,
        height=260,
        help="Enter each directed edge on a separate line, e.g. A B."
    )
    playback_speed = st.slider(
        "Autoplay delay (seconds)",
        min_value=0.2,
        max_value=2.0,
        value=0.8,
        step=0.1
    )
    if st.button("Restore Default Graph", use_container_width=True):
        st.session_state["graph_editor"] = DEFAULT_TEXT
        st.rerun()
# Use the sidebar editor's session state after reset.
if "graph_editor" not in st.session_state:
    st.session_state["graph_editor"] = edge_input
# The editor itself remains the source of graph input.
# Reset is handled below by the dedicated reset button.
try:
    graph = parse_edges(edge_input)
except ValueError as error:
    st.error(str(error))
    st.stop()

# ==================================================
# 7. SEARCH OPTIONS
# ==================================================

available_nodes = list(graph)

if "starting_node" not in st.session_state:
    st.session_state["starting_node"] = (
        "A" if "A" in available_nodes else available_nodes[0]
    )

if st.session_state["starting_node"] not in available_nodes:
    st.session_state["starting_node"] = available_nodes[0]

if "target_node" not in st.session_state:
    st.session_state["target_node"] = "No goal"

if st.session_state["target_node"] not in ["No goal"] + available_nodes:
    st.session_state["target_node"] = "No goal"

first, second, third = st.columns(3)

start_node = first.selectbox(
    "Starting node",
    available_nodes,
    key="starting_node"
)

goal_node = second.selectbox(
    "Goal node (optional)",
    ["No goal"] + available_nodes,
    key="target_node"
)

search_mode = third.selectbox(
    "Search method",
    ["Both", "BFS", "DFS"],
    key="search_method"
)

target = None if goal_node == "No goal" else goal_node

methods = ["BFS", "DFS"] if search_mode == "Both" else [search_mode]

outcomes = {
    method: run_search(graph, start_node, target, method)
    for method in methods
}


# ==================================================
# 8. SEARCH OUTPUT AND STEP INSPECTION
# ==================================================

for method, outcome in outcomes.items():

    st.divider()
    st.subheader(f"{method} Results")

    st.write(
        "**Expansion order:** "
        + " → ".join(outcome["order"])
    )

    if target is not None:
        st.write(
            "**Goal path:** "
            + (" → ".join(outcome["route"])
               if outcome["found"] else "Not reachable")
        )

    metric_a, metric_b, metric_c = st.columns(3)

    metric_a.metric("Expanded Nodes", outcome["total_expanded"])
    metric_b.metric("Largest Frontier", outcome["largest_frontier"])

    metric_c.metric(
        "Goal Path Edges",
        len(outcome["route"]) - 1
        if target is not None and outcome["found"]
        else "—"
    )

    chosen_step = st.slider(
        f"Inspect {method} expansion",
        min_value=1,
        max_value=len(outcome["trace"]),
        value=len(outcome["trace"]),
        key=f"inspect_{method}_{len(outcome['trace'])}"
    )

    autoplay = st.button(
        f"▶ Play {method}",
        key=f"autoplay_{method}"
    )

    graph_column, trace_column = st.columns([1.2, 1])

    with graph_column:
        graph_placeholder = st.empty()
        status_placeholder = st.empty()

    with trace_column:
        st.write("**Search Trace**")
        st.dataframe(
            pd.DataFrame(outcome["trace"]),
            hide_index=True,
            use_container_width=True
        )

    steps = (
        range(1, len(outcome["trace"]) + 1)
        if autoplay
        else [chosen_step]
    )

    for step_number in steps:
        figure = render_network(graph, outcome, step_number)
        graph_placeholder.pyplot(figure)
        plt.close(figure)

        record = outcome["trace"][step_number - 1]

        status_placeholder.info(
            f"Step {step_number}/{len(outcome['trace'])} | "
            f"Current: {record['Current Node']} | "
            f"Frontier: {record['Frontier']}"
        )

        if autoplay:
            time.sleep(playback_speed)

    st.write("**Node Levels and Parents**")

    level_table = pd.DataFrame([
        {
            "Node": node,
            "Level": outcome["levels"][node],
            "Parent": outcome["parents"][node] or "-",
            "Expansion Position": index + 1
        }
        for index, node in enumerate(outcome["order"])
    ])

    st.dataframe(
        level_table,
        hide_index=True,
        use_container_width=True
    )


# ==================================================
# 9. ALGORITHM COMPARISON
# ==================================================

if search_mode == "Both":

    st.divider()
    st.subheader("BFS and DFS Comparison")

    breadth = outcomes["BFS"]
    depth = outcomes["DFS"]

    comparison_data = {
        "Measure": [
            "Data Structure",
            "Expansion Order",
            "Expanded Nodes",
            "Maximum Frontier",
            "Deepest Level"
        ],
        "BFS": [
            "FIFO Queue",
            " → ".join(breadth["order"]),
            breadth["total_expanded"],
            breadth["largest_frontier"],
            max(breadth["levels"].values())
        ],
        "DFS": [
            "LIFO Stack",
            " → ".join(depth["order"]),
            depth["total_expanded"],
            depth["largest_frontier"],
            max(depth["levels"].values())
        ]
    }

    if target is not None:
        comparison_data["Measure"].extend([
            "Goal Path",
            "Goal Path Edges"
        ])

        comparison_data["BFS"].extend([
            " → ".join(breadth["route"]) or "Not reachable",
            len(breadth["route"]) - 1 if breadth["found"] else "—"
        ])

        comparison_data["DFS"].extend([
            " → ".join(depth["route"]) or "Not reachable",
            len(depth["route"]) - 1 if depth["found"] else "—"
        ])

    st.dataframe(
        pd.DataFrame(comparison_data),
        hide_index=True,
        use_container_width=True
    )

    if (
        target is not None
        and breadth["found"]
        and depth["found"]
        and len(breadth["route"]) < len(depth["route"])
    ):
        st.success(
            "BFS found a shorter path than DFS for this goal."
        )


# ==================================================
# 10. GRAPH SUMMARY
# ==================================================

st.divider()
st.subheader("Graph Summary")

summary_a, summary_b, summary_c = st.columns(3)

summary_a.metric("Total Nodes", len(graph))

summary_b.metric(
    "Directed Edges",
    sum(len(adjacent) for adjacent in graph.values())
)

summary_c.metric("Start Node", start_node)

st.caption("Interactive BFS and DFS learning tool.")
