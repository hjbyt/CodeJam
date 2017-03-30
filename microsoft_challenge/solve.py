import numpy as np
import networkx as nx

from io import StringIO
import sys

TEST = '''\
5
339,128,412,425,778
779,295,756,697,956
792,570,867,660,87
832,180,105,19,666
206,63,830,22,330
'''

# sys.stdin = StringIO(TEST)

N = 0


def main():
    rows = parse_input()
    r = solve(rows)
    print(r)


def parse_input():
    global N
    N = int(input())
    rows = []
    for i in range(1, N + 1):
        row = [int(x) for x in input().split(',')]
        if len(row) != N:
            raise AssertionError('unexpected')
        rows.append(row)
    if len(rows) != N:
        raise AssertionError('unexpected')
    return rows


def solve(rows):
    m = np.array(rows)

    adj = np.zeros((N ** 2, N ** 2))
    for i in range(N):
        for j in range(N):
            for x, y in neighbors(i, j):
                adj[point_to_index(i, j), point_to_index(x, y)] = m[x, y]

    G = nx.from_numpy_matrix(adj, create_using=nx.DiGraph())
    path = nx.dijkstra_path(G, 0, N ** 2 - 1)
    path = [index_to_point(a) for a in path]
    return sum(m[point] for point in path)


def neighbors(i, j):
    neighbors_ = []
    if i > 0:
        neighbors_.append((i - 1, j))
    if j > 0:
        neighbors_.append((i, j - 1))
    if i < N - 1:
        neighbors_.append((i + 1, j))
    if j < N - 1:
        neighbors_.append((i, j + 1))
    return neighbors_


def point_to_index(i, j):
    return i * N + j


def index_to_point(index):
    j = index % N
    i = index // N
    return i, j


if __name__ == '__main__':
    main()
