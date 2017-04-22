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
    # sys.stdin = open(r'inputs/input0_example.txt')
    # sys.stdout = Tee('test_out.txt')
    # sys.stdout = open('test_out.txt', 'w')

    cases = parse_input()

    for i, D, horses in cases:
        try:
            r = solve(D, horses)
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
        D, N = [int(x) for x in raw_input().split()]
        horses = []
        for _ in xrange(N):
            k, s = [int(x) for x in raw_input().split()]
            horses.append(Horse(pos=k, speed=s))
        yield i, D, horses


Horse = namedtuple('Horse', 'pos speed')


####################################

def solve(D, horses):
    horses.sort(key=lambda h: h.pos)
    horses.append(Horse(pos=D, speed=0))
    first_horse = horses[0]
    rest = horses[1:]
    segs = []
    for horse in reversed(rest):
        col = calc_collision(first_horse, horse)
        if col is None:
            continue
        if segs and col >= segs[-1][0]:
            continue
        else:
            segs.append((col, horse))

    segs.reverse()
    t = 0
    speed = first_horse.speed
    last_pos = first_horse.pos
    for col, horse in segs:
        d = col - last_pos
        t += d / speed
        speed = horse.speed
        last_pos = col
    return D / t




def calc_collision(h1, h2):
    return calc_collision_point__(h1.pos, h1.speed, h2.pos, h2.speed)


def calc_collision_point__(s1, k1, s2, k2):
    if s1 > s2:
        s1, k1, s2, k2 = s2, k2, s1, k1
    if k1 < k2 or (k1 == k2 and s1 < s2):
        return None
    return (s2 * k1 - s1 * k2) / float(k1 - k2)


if __name__ == '__main__':
    main()
