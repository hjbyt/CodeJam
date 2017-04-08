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

c2n = {
    '.': 0,
    '+': 1,
    'x': 2,
    'o': 3,
}
n2c = {v: k for k, v in c2n.items()}

n2v = {
    0: 0,
    1: 1,
    2: 1,
    3: 2,
}


def main():
    cases = parse_input()

    for i, b in cases:
        r = solve(b)
        print(f'Case #{i}: {r}')


def parse_input():
    T = int(input())
    for i in range(1, T + 1):
        N, M = [int(x) for x in input().split()]
        b = np.array([[b'.'] * N] * N)
        for _ in range(M):
            model, x, y = input().split()
            model = bytes(model, encoding='ascii')
            x, y = int(x) - 1, int(y) - 1
            b[x, y] = model
        yield i, b


def solve(b):
    print_board(b)


def print_board(b):
    for row in b:
        print(b''.join(row).decode())


if __name__ == '__main__':
    main()
