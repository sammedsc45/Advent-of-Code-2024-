from collections import deque


def load_byte_positions(filename, num_bytes=None):
    """Load byte positions from input file"""
    with open(filename, 'r') as f:
        byte_positions = [tuple(map(int, line.split(','))) for line in f.readlines()]
        return byte_positions if num_bytes is None else byte_positions[:num_bytes]


def simulate_memory_corruption(byte_positions, grid_size=70):
    """Simulate byte corruption in memory space"""
    memory_space = [['.' for _ in range(grid_size + 1)] for _ in range(grid_size + 1)]
    for x, y in byte_positions:
        if 0 <= x <= grid_size and 0 <= y <= grid_size:
            memory_space[y][x] = '#'
    return memory_space


def shortest_path(memory_space, start=(0, 0), end=(70, 70)):
    """Find shortest path from start to end using BFS"""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
    queue = deque([(start, 0)])  # (position, steps)
    visited = set([start])
    max_x, max_y = len(memory_space[0]) - 1, len(memory_space) - 1

    while queue:
        (x, y), steps = queue.popleft()
        if (x, y) == end:
            return steps
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx <= max_x) and (0 <= ny <= max_y) and memory_space[ny][nx] == '.' and (nx, ny) not in visited:
                queue.append(((nx, ny), steps + 1))
                visited.add((nx, ny))


def is_reachable(memory_space, start=(0, 0), end=(70, 70)):
    """Check if exit is reachable from start using BFS"""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
    queue = deque([(start, 0)])  # (position, steps)
    visited = set([start])
    max_x, max_y = len(memory_space[0]) - 1, len(memory_space) - 1

    while queue:
        (x, y), _ = queue.popleft()
        if (x, y) == end:
            return True
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx <= max_x) and (0 <= ny <= max_y) and memory_space[ny][nx] == '.' and (nx, ny) not in visited:
                queue.append(((nx, ny), 0))
                visited.add((nx, ny))
    return False


def find_first_blocking_byte(byte_positions):
    """Find the first byte that prevents the exit from being reachable"""
    memory_space = [['.' for _ in range(71)] for _ in range(71)]
    for i, (x, y) in enumerate(byte_positions):
        if 0 <= x <= 70 and 0 <= y <= 70:
            memory_space[y][x] = '#'
        if not is_reachable(memory_space):
            return f"{x},{y}"
    return "No blocking byte found"


def main():
    byte_positions = load_byte_positions('input.txt')

    # Part 1
    memory_space = simulate_memory_corruption(byte_positions[:1024], grid_size=70)
    min_steps = shortest_path(memory_space, end=(70, 70))
    print(f"Part 1: Minimum steps to reach exit: {min_steps}")

    # Part 2
    first_blocking_byte = find_first_blocking_byte(byte_positions)
    print(f"Part 2: First byte that prevents exit from being reachable: {first_blocking_byte}")


if __name__ == '__main__':
    main()
