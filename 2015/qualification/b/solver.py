from io import StringIO
import sys
import numpy as np

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
        Ps = np.array([int(x) for x in input().split()])
        if D != len(Ps):
            raise AssertionError('unexpected')
        yield i, Ps


def solve(Ps):
    m_index = np.argmax(Ps)
    m = Ps[m_index]

    if m <= 3:
        return m

    split(Ps, m_index)
    return min(solve(Ps) + 1, m)


def split(Ps, i):
    half = Ps[i] // 2
    Ps[i] -= half
    np.append(Ps, half)


def eat(Ps):
    Ps -= 1
    return np.delete(Ps, Ps == 0)


if __name__ == '__main__':
    main()
