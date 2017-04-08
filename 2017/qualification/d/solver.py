import numpy as np
from io import StringIO
import sys

TEST = '''\
3
2 0
1 1
o 1 1
3 4
+ 2 3
+ 2 1
x 3 1
+ 2 2
'''

sys.stdin = StringIO(TEST)

c2v = {
    '.': 0,
    '+': 1,
    'x': 1,
    'o': 2,
}


def main():
    cases = parse_input()

    for i, b in cases:
        r = solve(b)
        b, s = r
        print(f'Case #{i}: {s}')
        print(b)


def parse_input():
    T = int(input())
    for i in range(1, T + 1):
        N, M = [int(x) for x in input().split()]
        b = np.array([['.'] * N] * N)
        for _ in range(M):
            model, x, y = input().split()
            x, y = int(x) - 1, int(y) - 1
            b[x, y] = model
        yield i, b


def solve(b):
    s = style(b)
    cache = {board_string(b): s}
    return solve_brute(b, s, cache)


def solve_brute(b, s, cache):
    cache[board_string(b)] = style(b)
    N = len(b)
    for i in range(N):
        for j in range(N):
            if b[i, j] == '.':
                r = check(b, i, j)
                for c in r:
                    b[i, j] = c
                    s += c2v[c]
                    cache[board_string(b)] = s
                    solve_brute(b, s, cache)
                    b[i, j] = '.'
                    s -= c2v[c]
            elif b[i, j] != 'o':
                if 'o' in check(b, i, j):
                    old = b[i, j]
                    b[i, j] = 'o'
                    s += 1
                    cache[board_string(b)] = s
                    solve_brute(b, s, cache)
                    b[i, j] = old
                    s -= 1

    return max(cache.items(), key=lambda x: x[1])


def check(b, i, j):
    N = len(b)
    X, P, O = True, True, True
    for k in range(N):
        if b[k, j] in ['x', 'o'] or b[i, k] in ['x', 'o']:
            X = False
            O = False
            break

    for x, y in diag_points__(i, j, N):
        if b[x, y] in ['+', 'o']:
            P = False
            O = False
            break

    r = []
    if X:
        r.append('x')
    if P:
        r.append('+')
    if O:
        r.append('o')
    return r


def diag_points__(i, j, N):
    for k in range(1, N):
        p1 = add_diag(i, j, k)
        p2 = add_diag(i, j, -k)
        p3 = add_adiag(i, j, k)
        p4 = add_adiag(i, j, -k)
        if in_board(p1, N):
            yield p1
        if in_board(p2, N):
            yield p2
        if in_board(p3, N):
            yield p3
        if in_board(p4, N):
            yield p4


def in_board(k, N):
    return 0 <= k[0] < N and 0 <= k[1] < N


def add_diag(i, j, n):
    return i + n, j + n


def add_adiag(i, j, n):
    return i + n, j - n


def style(b):
    return sum(c2v[item] for sublist in b for item in sublist)


def board_string(b):
    return '\n'.join(''.join(row) for row in b)


if __name__ == '__main__':
    main()
