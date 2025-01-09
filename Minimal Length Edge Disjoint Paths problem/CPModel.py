#PYTHON 
import sys
from ortools.sat.python import cp_model
#import psutil
#process = psutil.Process()

def solve_edge_disjoint_paths(graph_edges, src, dst, n):
    model = cp_model.CpModel()

    adjacency = {i: [] for i in range(n)}
    for (u, v) in graph_edges:
        adjacency[u].append(v)
        
    #print(adjacency)

    x = {}
    for (u, v) in graph_edges:
        for p in [0, 1]:
            x[u, v, p] = model.NewBoolVar(f'x_{u}_{v}_{p}')
        model.Add(x[u, v, 0] + x[u, v, 1] <= 1)

    #for keys in x.keys():
        #print(keys)

    for p in [0, 1]:
        for node in range(n):
            inflow = sum(
                x[u, node, p] for u in adjacency if (u, node) in graph_edges
            )
            outflow = sum(
                x[node, v, p] for v in adjacency[node]
            )
            if node == src:
                model.Add(outflow - inflow == 1)
            elif node == dst:
                model.Add(inflow - outflow == 1)
            else:
                model.Add(inflow == outflow)

    total_length = sum(
        graph_edges[(u, v)] * (x[u, v, 0] + x[u, v, 1])
        for (u, v) in graph_edges
    )
    model.Minimize(total_length)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(int(solver.ObjectiveValue()))
    else:
        print('NOT_FEASIBLE')

def get_edges():
    n, m = map(int, sys.stdin.readline().split())
    graph_edges = {}
    for _ in range(m):
        u, v, w = map(int, sys.stdin.readline().split())
        u -= 1
        v -= 1
        if (u, v) not in graph_edges and (v, u) not in graph_edges:
            graph_edges[(u, v)] = w

    return graph_edges, n

graph_edges, n = get_edges()
#print(graph_edges)
solve_edge_disjoint_paths(graph_edges, 0, n - 1, n)

#print(f"Memory usage: {process.memory_info().rss // 1024 ** 2} MB")
