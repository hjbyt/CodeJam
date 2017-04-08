from heapq import heappush, heappop
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
    chunks = [-N]
    for _ in range(K):
        c = -heappop(chunks)
        c -= 1
        a = c // 2
        b = c - a
        heappush(chunks, -a)
        heappush(chunks, -b)
    return sorted([a, b], reverse=True)

if __name__ == '__main__':
    main()
