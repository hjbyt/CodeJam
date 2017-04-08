import networkx as nx

from io import StringIO
import sys

TEST = '''\
3
---+-++- 3
+++++ 4
-+-+- 4'''

# sys.stdin = StringIO(TEST)


def main():
    cases = parse_input()

    for i, S, K in cases:
        r = solve(S, K)
        print(f'Case #{i}: {r}')


def parse_input():
    T = int(input())
    for i in range(1, T + 1):
        S, K = input().split()
        S = [-1 if x == '-' else +1 for x in S]
        K = int(K)
        yield i, S, K


def solve(S, K):
    g = make_graph(S, K)
    dest = '+' * len(S)
    if not g.has_node(dest):
        return 'IMPOSSIBLE'
    else:
        return nx.shortest_path_length(g, to_string(S), dest)


def make_graph(S, K):
    g = nx.DiGraph()
    S_string = to_string(S)
    g.add_node(S_string)
    add_neighbours(S, S_string, K, g)
    return g


def add_neighbours(S, S_string, K, g):
    for i in range(0, len(S) - K + 1):
        flipped = flip(S, K, i)
        string = to_string(flipped)
        had_node = g.has_node(string)
        g.add_edge(S_string, string)
        if not had_node:
            add_neighbours(flipped, string, K, g)


def flip(S, K, i):
    S = S[:]
    for j in range(i, i + K):
        S[j] *= -1
    return S


def to_string(S):
    return ''.join('-' if x == -1  else '+' for x in S)


if __name__ == '__main__':
    main()
