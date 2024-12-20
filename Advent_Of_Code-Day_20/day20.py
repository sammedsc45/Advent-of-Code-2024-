from pathlib import Path
from time import time
from typing import Tuple, Dict, Set
from numbers import Complex

PICOSEC = 100


def parse_grid(file_path: str) -> Tuple[Dict[Complex, str], Complex, Complex]:
    """Parses the grid from the input file."""
    data: Dict[Complex, str] = {}
    start: Complex | None = None
    end: Complex | None = None
    try:
        with Path(file_path).open("r") as file:
            for i, line in enumerate(file):
                line = line.strip()
                for r, char in enumerate(line):
                    pos = complex(r, -i)
                    data[pos] = char
                    if char == "S":
                        start = pos
                        data[pos] = "."
                    elif char == "E":
                        end = pos
                        data[pos] = "."
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        exit(1)
    if not start or not end:
        print("Error: Could not find start or end position.")
        exit(1)
    return data, start, end


def get_race_path(grid: Dict[Complex, str], start: Complex, end: Complex) -> Dict[Complex, int]:
    """Finds the race path (shortest path) from start to end."""
    race: Dict[Complex, int] = {}
    previous: Complex | None = None
    position = start
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    i = 0
    while position != end:
        race[position] = i
        for dr, dc in moves:
            d = complex(dr, dc)
            if grid.get(position + d, "#") == "." and position + d != previous:
                previous = position
                position += d
                break
        i += 1
    race[end] = i
    return race


def get_reachable_positions(grid: Dict[Complex, str], pos: Complex, max_dist: int) -> Set[Tuple[int, Complex]]:
    """Returns set of reachable positions."""
    reached: Set[Tuple[int, Complex]] = set()
    for dist in range(1, max_dist + 1):
        for r in range(dist + 1):
            for d in (
                    complex(r, r - dist),
                    complex(r, -(r - dist)),
                    complex(-r, r - dist),
                    complex(-r, -(r - dist))
            ):
                new_pos = pos + d
                if grid.get(new_pos, "#") == ".":
                    reached.add((dist, new_pos))
    return reached


def calculate_cheats(race: Dict[Complex, int], grid: Dict[Complex, str], cheat_move: int) -> int:
    """Calculates the number of cheats that save at least PICOSEC time."""
    reachable_locations: Dict[Complex, Set[Tuple[int, Complex]]] = {}

    for pos in race:
        reachable_locations[pos] = get_reachable_positions(grid, pos, cheat_move)

    walls: Set[Tuple[Complex, Complex]] = set()
    for position, dist in race.items():
        for moves, cheat_pos in reachable_locations[position]:
            if grid.get(cheat_pos, "#") == "." and race[cheat_pos] - dist >= PICOSEC + moves:
                walls.add((position, cheat_pos))
    return len(walls)


if __name__ == "__main__":
    t = time()
    file_path = "input.txt"
    grid_data, start_pos, end_pos = parse_grid(file_path)
    race_path = get_race_path(grid_data, start_pos, end_pos)

    # Calculate and print for Part 1
    num_cheats_part1 = calculate_cheats(race_path, grid_data, 2)
    print(f"Part 1 Solution: {num_cheats_part1}")

    # Calculate and print for Part 2
    num_cheats_part2 = calculate_cheats(race_path, grid_data, 20)
    print(f"Part 2 Solution: {num_cheats_part2}")

    print(f"Total Time taken: {time() - t}")