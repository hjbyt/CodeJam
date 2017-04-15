from __future__ import print_function
import argparse
import atexit
import sys
import time
from contextlib import contextmanager
from collections import Counter

g_verbose = False
g_duration_counter = 1


def argmax(elements):
    return max(xrange(len(elements)), key=lambda x: elements[x])


@contextmanager
def measure():
    global g_duration_counter
    start = time.time()
    yield
    end = time.time()
    print('Duration #%d: %r' % (g_duration_counter, end - start), file=sys.stderr)
    g_duration_counter += 1


def measure_calls(func):
    def measured(*args, **kwargs):
        with measure():
            return func(*args, **kwargs)

    return measured


_g_measures = Counter()


class MeasureAll:
    def __init__(self, id):
        self.id = id

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        _g_measures[self.id] += time.time() - self.start


measure_all = MeasureAll


def print_measures():
    for id, total_time in _g_measures.iteritems():
        print('Total time (%s): %s' % (id, total_time), file=sys.stderr)


def measure_all_calls(func):
    def wrapper(*args, **kwargs):
        with measure_all('_func_calls_' + func.__name__):
            return func(*args, **kwargs)

    return wrapper


def log_calls(func):
    def logged(*args, **kwargs):
        print(args, kwargs)
        result = func(*args, **kwargs)
        print(result)
        return result

    return logged


class Tee(object):
    def __init__(self, name):
        self.file = open(name, 'w')
        self.stdout = sys.stdout
        sys.stdout = self

    def close(self):
        sys.stdout = self.stdout
        self.file.close()

    def write(self, data):
        self.file.write(data)
        self.file.flush()
        self.stdout.write(data)

    def flush(self):
        self.file.flush()
        self.stdout.flush()


####################################

def main():
    global g_verbose
    start_time = time.time()
    args = parse_args()
    g_verbose = args.verbose
    sys.stdin = args.input
    sys.stdout = args.output

    if args.print_time:
        atexit.register(print_measures)

    # TODO: XXX
    sys.stdin = open(r'inputs/input0_example.txt')
    sys.stdout = Tee('test_out.txt')
    # sys.stdout = open('test_out.txt', 'w')

    cases = parse_input()

    for i, N in cases:
        try:
            r = solve(N)
            print('Case #{i}: {r}'.format(i=i, r=r))
        except Exception:
            print('FAILED at case #%d' % (i + 1), file=sys.stderr)
            sys.stdout.flush()
            time.sleep(0.1)
            raise

    end_time = time.time()
    if args.print_time:
        print('Time: ' + str(end_time - start_time), file=sys.stderr)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=argparse.FileType('r'), nargs='?', default='-')
    parser.add_argument('output', type=argparse.FileType('w'), nargs='?', default='-')
    parser.add_argument('-t', dest='print_time', action='store_true')
    parser.add_argument('-v', dest='verbose', action='store_true')
    return parser.parse_args()


def parse_input():
    T = int(raw_input())
    for i in range(1, T + 1):
        N = int(raw_input())
        yield i, N


####################################

def solve(N):
    return solve_naive(N)


def solve_naive(N):
    return 0


if __name__ == '__main__':
    main()
