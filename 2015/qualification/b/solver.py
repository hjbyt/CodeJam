from io import StringIO
import sys

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

TEST = '''\
3
1
3
4
1 2 1 2
1
4
'''

# sys.stdin = StringIO(TEST)


def main():
    cases = parse_input()

    for i, Ps in cases:
        r = solve(Ps)
        print(f'Case #{i}: {r}')


def parse_input():
    T = int(input())
    for i in range(1, T + 1):
        D = int(input())
        Ps = [int(x) for x in input().split()]
        if D != len(Ps):
            raise AssertionError('unexpected')
        yield i, Ps


def solve(Ps):
    m = max(Ps)
    rs = []
    for n in range(1, m + 1):
        r = n + sum(ceildiv(x, n) - 1 for x in Ps)
        rs.append(r)
    return min(rs)


def ceildiv(a, b):
    return -(-a // b)


if __name__ == '__main__':
    main()
