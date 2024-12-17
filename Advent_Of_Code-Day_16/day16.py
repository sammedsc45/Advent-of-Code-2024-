import heapq


def read_grid(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    return [list(line) for line in lines]


def find_position(grid, char):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == char:
                return r, c
    return -1, -1


def dijkstra(grid):
    rows, cols = len(grid), len(grid[0])
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    start_r, start_c = find_position(grid, 'S')
    end_r, end_c = find_position(grid, 'E')
    start_direction = 1  # East

    min_costs = [[[float('inf')] * 4 for _ in range(cols)] for _ in range(rows)]
    min_costs[start_r][start_c][start_direction] = 0

    queue = [(0, start_r, start_c, start_direction)]

    while queue:
        cost, r, c, d = heapq.heappop(queue)

        if r == end_r and c == end_c:
            continue  # Reached end, but continue to find all paths

        # Move forward
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
            new_cost = cost + 1
            if new_cost < min_costs[nr][nc][d]:
                min_costs[nr][nc][d] = new_cost
                heapq.heappush(queue, (new_cost, nr, nc, d))

        # Turn right
        new_d = (d + 1) % 4
        new_cost = cost + 1000
        if new_cost < min_costs[r][c][new_d]:
            min_costs[r][c][new_d] = new_cost
            heapq.heappush(queue, (new_cost, r, c, new_d))

        # Turn left
        new_d = (d - 1) % 4
        new_cost = cost + 1000
        if new_cost < min_costs[r][c][new_d]:
            min_costs[r][c][new_d] = new_cost
            heapq.heappush(queue, (new_cost, r, c, new_d))

    return min_costs, end_r, end_c


def part_a(min_costs, end_r, end_c):
    minimal_cost = min(min_costs[end_r][end_c])
    print(f"Lowest score: {minimal_cost}")


def part_b(min_costs, grid, end_r, end_c):
    rows, cols = len(grid), len(grid[0])
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}

    # Find minimal cost to reach the end
    minimal_cost = min(min_costs[end_r][end_c])

    # Backward traversal to collect optimal positions
    queue = []
    for d in range(4):
        if min_costs[end_r][end_c][d] == minimal_cost:
            queue.append((end_r, end_c, d))

    visited = set()
    optimal_positions = set()

    while queue:
        r, c, d = queue.pop(0)
        if (r, c, d) in visited:
            continue
        visited.add((r, c, d))
        optimal_positions.add((r, c))

        # Previous state by moving forward
        dr, dc = directions[d]
        prev_r = r - dr
        prev_c = c - dc
        prev_d = d
        if 0 <= prev_r < rows and 0 <= prev_c < cols and grid[prev_r][prev_c] != '#':
            if min_costs[prev_r][prev_c][prev_d] + 1 == min_costs[r][c][d]:
                queue.append((prev_r, prev_c, prev_d))

        # Previous state by turning right or left to face direction d
        for turn_d in [(d - 1) % 4, (d + 1) % 4]:
            prev_r = r
            prev_c = c
            prev_d = turn_d
            if min_costs[prev_r][prev_c][prev_d] + 1000 == min_costs[r][c][d]:
                queue.append((prev_r, prev_c, prev_d))

    print(f"Number of tiles on optimal paths: {len(optimal_positions)}")


def main():
    grid = read_grid('input.txt')
    min_costs, end_r, end_c = dijkstra(grid)
    part_a(min_costs, end_r, end_c)
    part_b(min_costs, grid, end_r, end_c)


if __name__ == "__main__":
    main()
