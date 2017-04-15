from __future__ import print_function
import argparse
import atexit
import sys
import time
from contextlib import contextmanager
from collections import Counter, namedtuple

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

    for i, rows in cases:
        try:
            print('Case #{i}:'.format(i=i))
            solve(rows)
        except Exception:
            print('FAILED at case #%d' % i, file=sys.stderr)
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
        R, C = [int(x) for x in raw_input().split()]
        rows = []
        for _ in xrange(R):
            row = list(raw_input())
            rows.append(row)
        yield i, rows


####################################

def solve(rows):
    return solve_naive(rows)


g_initials = None


def solve_naive(rows):
    global g_initials
    g_initials = set(iter_cells(rows)) - set('?')
    fill(rows)
    rows = do_solve_naive(rows)
    print_rows(rows)
    g_initials = None


def do_solve_naive(rows):
    blank_point = get_blank(rows)
    if blank_point is None:
        return rows

    for initial in g_initials:
        finished_rows = try_with_initial(rows, blank_point, initial)
        if finished_rows is not None:
            return finished_rows


def try_with_initial(rows, blank_point, inital):
    rows = copy_rows(rows)
    try:
        rows[blank_point.y][blank_point.x] = inital
        fill(rows)
        return do_solve_naive(rows)
    except BadAttempt:
        return None


def get_blank(rows):
    for cell, point in iter_rows(rows):
        if cell == '?':
            return point
    return None


def print_rows(rows):
    print('\n'.join((''.join(row) for row in rows)))


def copy_rows(rows):
    return [row[:] for row in rows]


def fill(rows):
    for initial in g_initials:
        fill_for_initial(rows, initial)


class BadAttempt(Exception):
    pass


def fill_for_initial(rows, initial):
    points = [point for cell, point in iter_rows(rows) if cell == initial]
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    top_left = Point(x=min(xs), y=min(ys))
    bottom_right = Point(x=max(xs), y=max(ys))
    do_fill(rows, initial, top_left, bottom_right)


def do_fill(rows, initial, top_left, bottom_right):
    if not check_rect(rows, initial, top_left, bottom_right):
        raise BadAttempt()
    for y in xrange(top_left.y, bottom_right.y + 1):
        for x in xrange(top_left.x, bottom_right.x + 1):
            rows[y][x] = initial


def check_rect(rows, initial, top_left, bottom_right):
    for y in xrange(top_left.y, bottom_right.y + 1):
        for x in xrange(top_left.x, bottom_right.x + 1):
            current = rows[y][x]
            if current != '?' and current != initial:
                return False

    return True


class Point(namedtuple('Point', ['x', 'y'])):
    __slots__ = ()

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)


def iter_cells(rows):
    return (c for c, _ in iter_rows(rows))


def iter_rows(rows):
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            yield cell, Point(x, y)


if __name__ == '__main__':
    main()
