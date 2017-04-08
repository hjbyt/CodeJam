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
        r = solve2(N, K)
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


def solve2(N, K):
    if K == N:
        return 0, 0
    c = N - 1
    a = c // 2
    b = c - a
    if K == 1:
        return b, a

    if K == 2:
        return solve2(b, 1)

    if N % 2 == 1:
        if K % 2 == 1:
            return solve2((N - 1) // 2, (K - 1) // 2)
        else:
            return solve2((N - 1) // 2, (K - 1) // 2 + 1)

    k = K - 1
    ka = k // 2
    kb = k - ka
    sa = solve2(a, ka)
    sb = solve2(b, kb)
    return min([sa, sb], key=lambda x: (x[1], x[0]))


if __name__ == '__main__':
    main()
