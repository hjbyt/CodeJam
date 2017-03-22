from io import StringIO
import sys

TEST = '''\
4
4 11111
1 09
5 110011
0 1
'''

# sys.stdin = StringIO(TEST)


def main():
    cases = parse_input()

    for i, shyness in cases:
        r = solve(shyness)
        print(f'Case #{i}: {r}')


def parse_input():
    T = int(input())
    for i in range(1, T + 1):
        s_max, shyness = input().split()
        if int(s_max) != len(shyness) - 1:
            raise AssertionError('unexpected')
        shyness = [int(x) for x in shyness]
        yield i, shyness


def solve(shyness):
    r = 0
    s = 0
    for shyness, count in enumerate(shyness):
        if shyness > s:
            diff = shyness - s
            r += diff
            s += diff
        s += count
    return r


if __name__ == '__main__':
    main()
