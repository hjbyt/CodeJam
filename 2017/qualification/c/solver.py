from io import StringIO
import sys

TEST = '''\
5
4 2
5 2
6 2
1000 1000
1000 1
'''

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
    if K == N:
        return 0, 0

    n = N - 1
    a = n // 2
    b = n - a

    k = K - 1
    ka = k // 2
    kb = k - ka

    if K == 1:
        return b, a

    if K == 2:
        return solve(b, 1)

    if n % 2 == 0:
        return solve(b, kb)
    else:
        if k % 2 == 0:
            return solve(a, ka)
        else:
            return solve(b, kb)


if __name__ == '__main__':
    main()
