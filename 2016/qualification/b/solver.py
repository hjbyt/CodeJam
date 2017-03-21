def main():
    cases = parse_input()

    for i, stack in cases:
        r = solve3(stack)
        print(f'Case #{i}: {r}')


def parse_input():
    T = int(input())
    for i in range(1, T + 1):
        stack = input()
        stack = [-1 if x == '-' else +1 for x in stack]
        yield i, stack


def flip(stack, count):
    if not (0 <= count < len(stack)):
        raise ValueError("invalid count")
    return [-1 * x for x in reversed(stack[:count])] + stack[:count]


def solve(stack, target=+1):
    if len(stack) == 0:
        return 0
    if stack[-1] == target:
        return solve(stack[:-1], target=target)
    else:
        return solve(stack[:-1], target=-target) + 1


def solve2(stack, target=+1, count=0):
    if len(stack) == 0:
        return count
    if stack[-1] == target:
        return solve2(stack[:-1], target=target, count=count)
    else:
        return solve2(stack[:-1], target=-target, count=count + 1)


def solve3(stack):
    target = +1
    count = 0
    last_index = len(stack) - 1
    while last_index >= 0:
        if stack[last_index] != target:
            count += 1
            target *= -1
        last_index -= 1
    return count


if __name__ == '__main__':
    main()
