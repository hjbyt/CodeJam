from io import StringIO
import sys

TEST = '''\
4
132
1000
7
111111111111111110'''

# sys.stdin = StringIO(TEST)


def main():
    cases = parse_input()

    for i, N in cases:
        r = solve(N)
        print(f'Case #{i}: {r}')


def parse_input():
    T = int(input())
    for i in range(1, T + 1):
        N = int(input())
        yield i, N


def solve(N):
    n = [int(x) for x in str(N)]
    while True:
        for i, (digit, next_digit) in enumerate(zip(n, n[1:])):
            if digit > next_digit:
                break
        else:
            return int(''.join(str(x) for x in n))

        n[i] -= 1
        for j in range(i+1, len(n)):
            n[j] = 9


if __name__ == '__main__':
    main()
