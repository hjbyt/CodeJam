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
    last_index = len(S) - K
    c = 0
    for i in range(last_index):
        if S[i] != +1:
            flip(S, K, i)
            c += 1
    last = S[last_index:]
    if len(last) != K:
        raise Exception('unexpected')
    if all(x == +1 for x in last):
        return c
    elif all(x == -1 for x in last):
        return c + 1
    else:
        return 'IMPOSSIBLE'


def flip(S, K, i):
    for j in range(i, i + K):
        S[j] *= -1


if __name__ == '__main__':
    main()
