import numpy as np
from io import StringIO
import sys

TEST = '''\
5
4 2
5 2
6 2
1000 1000
1000 1'''

# sys.stdin = StringIO(TEST)


def main():
    cases = parse_input()

    for i, N, K in cases:
        r = solve(N, K)
        r = ' '.join(str(x) for x in r)
        print(f'Case #{i}: {r}')


def parse_input():
    T = int(input())
    for i in range(1, T + 1):
        N, K = [int(x) for x in input().split()]
        yield i, N, K


def solve(N, K):
    chunks = np.array([N])
    for _ in range(K):
        i = np.argmax(chunks)
        c = chunks[i] - 1
        a = c // 2
        b = c - a
        chunks[i] = a
        chunks = np.insert(chunks, i + 1, b)
    return sorted([a, b], reverse=True)

if __name__ == '__main__':
    main()
