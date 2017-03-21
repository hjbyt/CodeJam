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
    if N == 0:
        return 'INSOMNIA'
    x = 0
    digits = set()
    while len(digits) < 10:
        x += N
        digits |= set(str(x))
    return x


if __name__ == '__main__':
    main()
