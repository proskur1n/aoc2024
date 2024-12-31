from copy import deepcopy

class Graph:
    def __init__(self):
        self.forward = {}

    def add_edge(self, a, b):
        self.forward.setdefault(a, []).append(b)

    def node_subset(self, nodes):
        subset = {}
        for node, successors in self.forward.items():
            if node in nodes:
                subset[node] = [s for s in successors if s in nodes]
        g = Graph()
        g.forward = subset
        return g

    def with_edges(self, edges):
        g = Graph()
        g.forward = deepcopy(self.forward)
        for a, b in edges:
            g.add_edge(a, b)
        return g

    def topological_sort(self):
        def dfs(node, visited):
            visited.add(node)
            for neighbor in self.forward.get(node, []):
                if neighbor in visited:
                    # cycle
                    raise StopIteration()
                if neighbor in unmarked:
                    unmarked.remove(neighbor)
                    dfs(neighbor, visited)
            visited.remove(node)
            ordered.append(node)

        ordered = []
        unmarked = set(self.forward).union(*self.forward.values())
        try:
            while len(unmarked) > 0:
                dfs(unmarked.pop(), set())
        except StopIteration:
            return "cycle"
        return ordered[::-1]

with open("input") as file:
    rules, updates = file.read().split("\n\n")
    rules = rules.strip().split("\n")
    updates = updates.strip().split("\n")

    graph = Graph()
    for rule in rules:
        a, b = rule.split("|")
        graph.add_edge(a, b)

    sumPartOne = 0
    sumPartTwo = 0

    for update in updates:
        pages = update.split(",")

        # Ordering relation in "input" has cycles :/
        subset = graph.node_subset(pages)

        if subset.with_edges(zip(pages, pages[1:])).topological_sort() != "cycle":
            sumPartOne += int(pages[len(pages)//2])
        else:
            pages = subset.topological_sort()
            sumPartTwo += int(pages[len(pages)//2])

    print("Part One:", sumPartOne)
    print("Part Two:", sumPartTwo)
