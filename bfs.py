
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time
from collections import deque

GRAPH = {
    'A': ['B', 'D'], 'B': ['C', 'E', 'G'],
    'C': ['A'], 'D': ['C'], 'E': ['H'],
    'F': [], 'G': ['F'], 'H': ['F', 'G']
}

DEFAULT_EDGES = "\n".join(
    f"{u} {v}" for u, vs in GRAPH.items()
    for v in (vs if vs else [None]) if v is not None
) + "\nF"

DEFAULTS = {
    "edges": DEFAULT_EDGES,
    "start": "A",
    "goal": "No goal",
    "method": "Both",
    "speed": 0.8
}

st.set_page_config(
    page_title="BSD3513 | Lab Report 1",
    page_icon="🔎",
    layout="wide"
)


def reset():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value
    for key in list(st.session_state):
        if key.startswith(("BFS_step", "DFS_step")):
            del st.session_state[key]


def parse_graph(text):
    graph = {}

    for line in text.splitlines():
        line = line.split("#")[0].strip().replace(",", " ")
        if not line:
            continue

        parts = line.upper().split()
        if len(parts) not in (1, 2):
            raise ValueError(f"Invalid line: {line}")

        source = parts[0]
        graph.setdefault(source, [])

        if len(parts) == 2:
            graph[source].append(parts[1])
            graph.setdefault(parts[1], [])

    if not graph:
        raise ValueError("Graph cannot be empty.")
    if len(graph) > 100:
        raise ValueError("Maximum 100 nodes.")

    return {
        node: sorted(set(neighbors))
        for node, neighbors in sorted(graph.items())
    }


def search(graph, start, goal, method):
    frontier = deque([start]) if method == "BFS" else [start]
    discovered = {start}
    parent = {start: None}
    depth = {start: 0}
    order, trace = [], []

    while frontier:
        node = frontier.popleft() if method == "BFS" else frontier.pop()
        order.append(node)

        if node != goal:
            neighbors = graph[node]
            if method == "DFS":
                neighbors = list(reversed(neighbors))

            for neighbor in neighbors:
                if neighbor not in discovered:
                    discovered.add(neighbor)
                    parent[neighbor] = node
                    depth[neighbor] = depth[node] + 1
                    frontier.append(neighbor)

        trace.append({
            "Step": len(trace) + 1,
            "Current": node,
            "Visited": " → ".join(order),
            "Frontier": str(list(frontier)),
            "Depth": depth[node],
            "Parent": parent[node] or "-"
        })

        if node == goal:
            break

    path = []
    if goal in order:
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()

    return {
        "order": order,
        "path": path,
        "found": goal in order,
        "trace": trace,
        "depth": depth,
        "explored": len(order),
        "max_frontier": max(
            len(t["Frontier"].strip("[]").split(","))
            if t["Frontier"] != "[]" else 0
            for t in trace
        ) if trace else 0
    }


def draw_graph(graph, result, step):
    g = nx.DiGraph()
    for node, neighbors in graph.items():
        g.add_node(node)
        for neighbor in neighbors:
            g.add_edge(node, neighbor)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    pos = nx.spring_layout(g, seed=13)

    current = result["trace"][step - 1]["Current"]
    visited = result["order"][:step]

    colors = [
        "#10b981" if n == current
        else "#93c5fd" if n in visited
        else "#e5e7eb"
        for n in g.nodes()
    ]

    nx.draw_networkx(
        g, pos, ax=ax, with_labels=True,
        node_color=colors, node_size=900,
        font_weight="bold", arrows=True,
        arrowsize=18, edge_color="#64748b"
    )
    ax.axis("off")
    return fig


for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)


st.title("BFS & DFS | Interactive Uninformed Search")
st.caption("BSD3513 Artificial Intelligence · Lab Report 1 · UMPSA")

with st.expander("Learning Guide"):
    st.markdown("""
    - **BFS:** FIFO queue; explores level by level.
    - **DFS:** LIFO stack; explores deeper branches first.
    - Both have O(V + E) time complexity using an adjacency list.
    - BFS finds a shortest path in an unweighted graph.
    """)

with st.sidebar:
    st.header("Graph Editor")
    st.text_area("Directed edges (one per line: A B)",
                 key="edges", height=250)
    st.caption("Use one node per line for an isolated node.")
    st.slider("Autoplay speed (seconds)", 0.2, 2.0,
              step=0.1, key="speed")
    st.button("Reset to Default", on_click=reset)

try:
    graph = parse_graph(st.session_state.edges)
except ValueError as error:
    st.error(str(error))
    st.stop()

nodes = list(graph)

if st.session_state.start not in nodes:
    st.session_state.start = nodes[0]
if st.session_state.goal not in ["No goal"] + nodes:
    st.session_state.goal = "No goal"

col1, col2, col3 = st.columns(3)
start = col1.selectbox("Starting Node", nodes, key="start")
goal_option = col2.selectbox(
    "Goal Node", ["No goal"] + nodes, key="goal"
)
method = col3.selectbox(
    "Algorithm", ["Both", "BFS", "DFS"], key="method"
)

goal = None if goal_option == "No goal" else goal_option
algorithms = ["BFS", "DFS"] if method == "Both" else [method]

results = {
    name: search(graph, start, goal, name)
    for name in algorithms
}

for name, result in results.items():
    st.subheader(f"{name} Search")
    st.write("**Expansion Order:** " + " → ".join(result["order"]))

    if goal:
        path = " → ".join(result["path"]) if result["found"] else "Not reachable"
        st.write("**Goal Path:** " + path)

    a, b, c = st.columns(3)
    a.metric("Expanded Nodes", result["explored"])
    b.metric("Maximum Frontier", result["max_frontier"])
    c.metric(
        "Path Edges",
        len(result["path"]) - 1 if result["found"] else "—"
    )

    step = st.slider(
        f"{name} Step", 1, len(result["trace"]),
        len(result["trace"]), key=f"{name}_step"
    )

    autoplay = st.button(f"▶ Autoplay {name}", key=f"play_{name}")

    left, right = st.columns([1.2, 1])
    graph_area = left.empty()
    info_area = left.empty()

    right.write("**Step Trace**")
    right.dataframe(
        pd.DataFrame(result["trace"]),
        hide_index=True,
        use_container_width=True
    )

    steps = range(1, len(result["trace"]) + 1) if autoplay else [step]

    for current_step in steps:
        fig = draw_graph(graph, result, current_step)
        graph_area.pyplot(fig)
        plt.close(fig)

        current = result["trace"][current_step - 1]
        info_area.info(
            f"Step {current_step} | Current: {current['Current']} | "
            f"Frontier: {current['Frontier']}"
        )

        if autoplay and current_step < len(result["trace"]):
            time.sleep(st.session_state.speed)

st.divider()

if method == "Both":
    st.subheader("BFS vs DFS Comparison")
    bfs, dfs = results["BFS"], results["DFS"]

    comparison = pd.DataFrame({
        "Measure": [
            "Data Structure", "Expansion Order", "Expanded Nodes",
            "Maximum Frontier", "Deepest Level", "Goal Path"
        ],
        "BFS": [
            "FIFO Queue", " → ".join(bfs["order"]),
            bfs["explored"], bfs["max_frontier"],
            max(bfs["depth"].values()),
            " → ".join(bfs["path"]) or "Not reachable"
        ],
        "DFS": [
            "LIFO Stack", " → ".join(dfs["order"]),
            dfs["explored"], dfs["max_frontier"],
            max(dfs["depth"].values()),
            " → ".join(dfs["path"]) or "Not reachable"
        ]
    })

    st.dataframe(comparison, hide_index=True, use_container_width=True)

    if goal and bfs["found"] and dfs["found"]:
        bfs_edges = len(bfs["path"]) - 1
        dfs_edges = len(dfs["path"]) - 1

        if bfs_edges < dfs_edges:
            st.success(
                f"BFS found a shorter path: {bfs_edges} edges "
                f"compared with DFS's {dfs_edges} edges."
            )
