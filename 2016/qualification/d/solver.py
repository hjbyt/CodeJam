from functools import wraps
from io import StringIO
import sys


# sys.stdin = StringIO('''5
# 2 3 2
# 1 1 1
# 2 1 1
# 2 1 2
# 3 2 3''')

# from http://stackoverflow.com/a/12377059
def listify(fn=None, wrapper=list):
    """
    A decorator which wraps a function's return value in ``list(...)``.

    Useful when an algorithm can be expressed more cleanly as a generator but
    the function should return an list.

    Example::

        >>> @listify
        ... def get_lengths(iterable):
        ...     for i in iterable:
        ...         yield len(i)
        >>> get_lengths(["spam", "eggs"])
        [4, 4]
        >>>
        >>> @listify(wrapper=tuple)
        ... def get_lengths_tuple(iterable):
        ...     for i in iterable:
        ...         yield len(i)
        >>> get_lengths_tuple(["foo", "bar"])
        (3, 3)
    """

    def listify_return(fn):
        @wraps(fn)
        def listify_helper(*args, **kw):
            return wrapper(fn(*args, **kw))

        return listify_helper

    if fn is None:
        return listify_return
    return listify_return(fn)


def print_list(list):
    for x in list:
        print(x)


def is_L(pattern, i, C):
    # Note: not correct
    K = len(pattern)
    for j in range(1, C+1):
        if pattern[(i // C**(j-1)) % K] != 'L':
            return False
    else:
        return True


def check(pattern, i, C):
    return 'L' if is_L(pattern, i, C) else 'G'


def gen2(pattern, C):
    return ''.join(check(pattern, i, C) for i in range(len(pattern) ** C))

def gen_all2(K, C):
    for pattern in hard_patterns(K):
        print(pattern + ':', gen2(pattern, C))

def main():
    # gen_all(K=3, C=2)
    # print()
    # gen_all2(K=3, C=2)
    # exit()

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
    assert S < K
    if C == 1:
        return None

    return None


def gen_all(K, C):
    for pattern in hard_patterns(K):
        print(pattern + ':', gen(pattern, C))


@listify
def all_patterns(K):
    for i in range(2 ** K):
        p = bin(i)[2:].zfill(K)
        yield p.replace('0', 'G').replace('1', 'L')


@listify
def hard_patterns(K):
    for i in range(K):
        p = bin(2 ** i)[2:].zfill(K)
        yield p.replace('0', 'L').replace('1', 'G')


def gen(pattern, C):
    s = pattern
    for _ in range(C - 1):
        s = ''.join([rep(t, pattern) for t in s])
    return s


def rep(tile, pattern):
    if tile == 'L':
        return pattern
    else:
        return 'G' * len(pattern)


if __name__ == '__main__':
    main()
