import random
import sympy.ntheory as nt

from io import StringIO
import sys
# sys.stdin = StringIO('''1
# 32 1''')


def main():
    cases = parse_input()

    for i, N, J in cases:
        r = solve(N, J)
        print(f'Case #{i}:')
        for a, divisors in r.items():
            nums = [a] + divisors
            print(' '.join(str(x) for x in nums))


def parse_input():
    T = int(input())
    for i in range(1, T + 1):
        N, J = [int(x) for x in input().split()]
        yield i, N, J


def solve(N, J):
    results = {}
    i = 0
    while len(results) < J:
        print(f'#{i}', file=sys.stderr)
        a, nums = find(N)
        divisors = [get_divisor(x) for x in nums]
        results[a] = divisors
        i += 1
    return results


def find(N):
    while True:
        a = random.randint(1, 2 ** (N - 2))
        a = '1' + bin(a)[2:].zfill(N - 2) + '1'
        nums = [as_base(a, base) for base in range(2, 10 + 1)]
        if any(map(nt.isprime, nums)):
            continue
        else:
            return a, nums


def as_base(string, base):
    r = 0
    d = 1
    for b in reversed(string):
        r += int(b) * d
        d *= base
    return r


def get_divisor(num):
    print(f'get_divisor({num})', file=sys.stderr)
    return nt.pollard_rho(num)
    # for d in nt.divisors(num, generator=True):
    #     if d not in [1, num]:
    #         return d
    # else:
    #     raise ValueError('num is prime')


if __name__ == '__main__':
    main()
