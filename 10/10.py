import networkx as nx

with open("input") as file:
    height = [list(map(int, line)) for line in file.read().strip().split("\n")]

g = nx.grid_2d_graph(len(height), len(height[0]), create_using=nx.DiGraph)
for (x, y), d in g.nodes(data=True):
    d["height"] = height[y][x]
g = nx.subgraph_view(g, filter_edge=lambda u, v: g.nodes[u]["height"] + 1 == g.nodes[v]["height"])

trailheads = [n for n, d in g.nodes(data=True) if d["height"] == 0]
peaks = {s: nx.descendants_at_distance(g, s, 9) for s in trailheads}

print(sum(map(len, peaks.values())))

# Very slow solution but I wanted to use built-in networkx functions today.
print(sum(sum(1 for _ in nx.all_simple_paths(g, s, t)) for s in trailheads for t in peaks[s]))
