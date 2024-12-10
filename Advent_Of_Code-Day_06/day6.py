import copy
from collections import defaultdict
from enum import Enum
from typing import Dict, Tuple, Optional, List

SIZE = 130  # Adjust based on your input file size


class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def turn_right(self):
        return [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH][
            list(Direction).index(self)
        ]


def generate_map(filename: str) -> Optional[Tuple[Dict[Tuple[int, int], str], int, int]]:
    """Generates a map from the input file."""
    map_data = defaultdict(str)
    max_x, max_y = 0, 0
    try:
        with open(filename, 'r') as f:
            for y, line in enumerate(f):
                for x, char in enumerate(line.strip()):
                    map_data[(x, y)] = char
                    max_x, max_y = max(max_x, x), max(max_y, y)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    return map_data, max_x, max_y


def solve_part_one(map_data: Dict[Tuple[int, int], str], max_x: int, max_y: int) -> int:
    """Solves Part One - Traversing the map."""
    start_loc = next(coord for coord, char in map_data.items() if char == '^')
    visited = set()
    direction = Direction.NORTH

    while 0 <= start_loc[0] <= max_x and 0 <= start_loc[1] <= max_y:
        visited.add(start_loc)
        next_loc = (start_loc[0] + direction.value[0], start_loc[1] + direction.value[1])

        while (0 <= next_loc[0] <= max_x and 0 <= next_loc[1] <= max_y and
               map_data.get(next_loc) == '#'):
            direction = direction.turn_right()
            next_loc = (start_loc[0] + direction.value[0], start_loc[1] + direction.value[1])

        start_loc = (start_loc[0] + direction.value[0], start_loc[1] + direction.value[1])

    return len(visited)


def solve_part_two(filename: str) -> int:
    """Solves Part Two - Placing obstacles."""
    # Create 2D lists for map, direction tracking, and obstacles
    map_grid = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]
    dir_map = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    obstacle_map = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

    # Read input file
    with open(filename, "r") as f:
        for r in range(SIZE):
            line = f.readline().strip()
            for c, char in enumerate(line):
                map_grid[r][c] = char
                if char == '^':
                    guard_row, guard_col = r, c

    def solve_recursive(guard_row: int, guard_col: int, direction: int,
                        depth: int, map_state: List[List[str]],
                        dir_state: List[List[int]],
                        obstacle_state: List[List[int]]) -> int:
        count = 0

        while True:
            if depth == 1 and map_state[guard_row][guard_col] == 'X' and \
                    ((1 << direction) & dir_state[guard_row][guard_col]) != 0:
                return 1

            map_state[guard_row][guard_col] = 'X'
            dir_state[guard_row][guard_col] |= 1 << direction

            next_row, next_col = guard_row, guard_col

            if direction == 0:  # NORTH
                next_row -= 1
            elif direction == 1:  # EAST
                next_col += 1
            elif direction == 2:  # SOUTH
                next_row += 1
            elif direction == 3:  # WEST
                next_col -= 1

            if 0 <= next_row < SIZE and 0 <= next_col < SIZE:
                if map_state[next_row][next_col] == '#':
                    direction = (direction + 1) % 4
                elif depth == 0 and map_state[next_row][next_col] != 'X' and not obstacle_state[next_row][next_col]:
                    new_map = copy.deepcopy(map_state)
                    new_dir_map = copy.deepcopy(dir_state)
                    new_map[next_row][next_col] = '#'
                    obstacle = solve_recursive(guard_row, guard_col,
                                               (direction + 1) % 4, 1,
                                               new_map, new_dir_map,
                                               obstacle_state)
                    if obstacle:
                        obstacle_state[next_row][next_col] = 1
                        count += 1
                    guard_row, guard_col = next_row, next_col
                else:
                    guard_row, guard_col = next_row, next_col
            else:
                break

        return count if depth == 0 else 0

    # Solve Part Two
    return solve_recursive(guard_row, guard_col, 0, 0, map_grid, dir_map, obstacle_map)


def main():
    filename = "input.txt"  # Replace with your input filename

    # Part One
    map_data_result = generate_map(filename)
    if map_data_result:
        map_data, max_x, max_y = map_data_result
        result_part_one = solve_part_one(map_data, max_x, max_y)
        print(f"Part One: {result_part_one}")

    # Part Two
    result_part_two = solve_part_two(filename)
    print(f"Part Two: {result_part_two}")


if __name__ == "__main__":
    main()