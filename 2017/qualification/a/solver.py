from io import StringIO
import sys

TEST = '''\
3
---+-++- 3
+++++ 4
-+-+- 4'''

sys.stdin = StringIO(TEST)


def main():
    cases = parse_input()

    for i, S, K in cases:
        r = solve(S, K)
        print(f'Case #{i}: {r}')


def parse_input():
    T = int(input())
    for i in range(1, T + 1):
        S, K = input().split()
        K = int(K)
        yield i, S, K


def solve(S, K):
    pass


if __name__ == '__main__':
    main()
