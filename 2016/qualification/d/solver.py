from io import StringIO
import sys

# sys.stdin = StringIO('''5
# 2 3 2
# 1 1 1
# 2 1 1
# 2 1 2
# 3 2 3''')


def main():
    cases = parse_input()

    for i, K, C, S in cases:
        r = solve(K, C, S)
        if r is None:
            r = 'IMPOSSIBLE'
        else:
            r = ' '.join(str(x) for x in r)
        print(f'Case #{i}: {r}')


def parse_input():
    T = int(input())
    for i in range(1, T + 1):
        K, C, S = [int(x) for x in input().split()]
        yield i, K, C, S


def solve(K, C, S):
    if K == S:
        return list(range(1, K + 1))
    else:
        return None


if __name__ == '__main__':
    main()
