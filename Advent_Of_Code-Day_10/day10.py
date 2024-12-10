from collections import deque


def parse_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    height_map = []
    for line in lines:
        height_map.append([int(char) for char in line.strip()])
    return height_map


def find_trailheads(height_map):
    trailheads = []
    for r, row in enumerate(height_map):
        for c, value in enumerate(row):
            if value == 0:
                trailheads.append((r, c))
    return trailheads


def bfs_part1(height_map, start):
    """
    Part 1: Calculate the score (number of reachable 9s) for a trailhead.
    """
    rows, cols = len(height_map), len(height_map[0])
    visited = set()
    queue = deque([start])
    visited.add(start)
    reachable_nines = 0
    while queue:
        r, c = queue.popleft()
        if height_map[r][c] == 9:
            reachable_nines += 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if height_map[nr][nc] == height_map[r][c] + 1:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
    return reachable_nines


def bfs_part2(height_map, start):
    """
    Part 2: Calculate the rating (number of distinct hiking trails) for a trailhead.
    """
    rows, cols = len(height_map), len(height_map[0])
    visited = set()
    queue = deque([(start, [])])
    visited.add((start, tuple()))
    trails = set()

    while queue:
        (r, c), path = queue.popleft()
        path = path + [(r, c)]
        if height_map[r][c] == 9:
            trails.add(tuple(path))
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if height_map[nr][nc] == height_map[r][c] + 1:
                    new_path = path + [(nr, nc)]
                    if (nr, nc, tuple(new_path)) not in visited:
                        visited.add((nr, nc, tuple(new_path)))
                        queue.append(((nr, nc), path))
    return len(trails)


def part1(height_map):
    trailheads = find_trailheads(height_map)
    total_score = 0
    for trailhead in trailheads:
        score = bfs_part1(height_map, trailhead)
        total_score += score
    return total_score


def part2(height_map):
    trailheads = find_trailheads(height_map)
    total_rating = 0
    for trailhead in trailheads:
        rating = bfs_part2(height_map, trailhead)
        total_rating += rating
    return total_rating


def main(file_path):
    height_map = parse_input(file_path)
    result_part1 = part1(height_map)
    result_part2 = part2(height_map)
    print(f"Part 1: The sum of the scores of all trailheads is: {result_part1}")
    print(f"Part 2: The sum of the ratings of all trailheads is: {result_part2}")


if __name__ == "__main__":
    file_path = 'input.txt'  # Replace with the path to your input file
    main(file_path)
