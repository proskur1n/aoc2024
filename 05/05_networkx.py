import networkx as nx

with open("input") as file:
    rules, updates = file.read().split("\n\n")
    rules = rules.strip().split("\n")
    updates = updates.strip().split("\n")

    graph = nx.DiGraph(rule.split("|") for rule in rules)

    sumCorrect = 0
    sumIncorrect = 0

    for update in updates:
        pages = update.split(",")

        # Ordering relation in "input" has cycles :/
        g = graph.subgraph(pages)

        try:
            copy = g.copy()
            copy.add_edges_from(zip(pages, pages[1:]))
            s = list(nx.topological_sort(copy))
            sumCorrect += int(pages[len(pages)//2])
        except nx.NetworkXUnfeasible: # Cycle in the topological sort.
            s = list(nx.topological_sort(g))
            sumIncorrect += int(s[len(s)//2])

    print(sumCorrect, sumIncorrect)
