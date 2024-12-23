from collections import defaultdict

with open('input/23.txt') as f:
    lines = [line.strip().split('-') for line in f.readlines()]

links = set()
graph = defaultdict(list)
for c1, c2 in lines:
    links.add((c1, c2))
    links.add((c2, c1))
    graph[c1].append(c2)
    graph[c2].append(c1)


def part1():
    triads = set()
    for c1, clist in graph.items():
        if not c1.startswith('t'): continue
        for i, c2 in enumerate(clist):
            for j in range(i + 1, len(clist)):
                c3 = clist[j]
                if (c2, c3) in links:
                    triad = tuple(sorted([c1, c2, c3]))
                    triads.add(triad)
    print(len(triads))


def part2():
    cliques = []
    bron_kerbosch(set(), set(graph.keys()), set(), cliques)
    max_len = max((len(c) for c in cliques))
    max_clique = next(c for c in cliques if len(c) == max_len)
    print(','.join(sorted(max_clique)))


def bron_kerbosch(clique, candidates, visited, out_cliques):
    if not candidates and not visited:
        out_cliques.append(clique)
        return

    for n in list(candidates):
        n_edges = set(graph[n])
        bron_kerbosch(clique | {n}, candidates & n_edges, visited & n_edges, out_cliques)
        candidates.remove(n)
        visited.add(n)


part1()
part2()
