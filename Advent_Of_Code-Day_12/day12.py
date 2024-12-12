import sys
from itertools import product

# Constants
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
CORNER_PATTERNS = [
    (lambda n: n[1][0] == 0 and n[0][1] == 0),
    (lambda n: n[0][0] == 0 and n[1][0] == 1 and n[0][1] == 1),
    (lambda n: n[1][2] == 0 and n[0][1] == 0),
    (lambda n: n[0][2] == 0 and n[1][2] == 1 and n[0][1] == 1),
    (lambda n: n[1][0] == 0 and n[2][1] == 0),
    (lambda n: n[2][0] == 0 and n[1][0] == 1 and n[2][1] == 1),
    (lambda n: n[1][2] == 0 and n[2][1] == 0),
    (lambda n: n[2][2] == 0 and n[1][2] == 1 and n[2][1] == 1)
]
CELL_SIZE = 3

class Region:
    def __init__(self, idx: str, start_position: tuple[int, int]) -> None:
        self.idx = idx
        self.positions = {start_position}
        self.perimeter = 0
        self.corners = 0

    def price(self) -> int:
        return len(self.positions) * self.perimeter

    def side_price(self) -> int:
        return len(self.positions) * self.corners

    def __repr__(self) -> str:
        return f"Region {self.idx} in positions {self.positions}"


class Field:
    def __init__(self, field_map: list[str]) -> None:
        self.field_map = field_map
        self.regions = []
        self.remaining = set(product(range(len(field_map)), range(len(field_map[0]))))
        self._rows, self._cols = len(field_map), len(field_map[0])

        while self.remaining:
            self.fill_region()

    def fill_region(self) -> None:
        position = self.remaining.pop()
        queue, visited = {position}, set()
        idx = self.field_map[position[0]][position[1]]
        region = Region(idx, position)

        while queue:
            position = queue.pop()
            visited.add(position)
            region.corners += self.count_corners(position)

            for direction in DIRECTIONS:
                next_position = (position[0] + direction[0], position[1] + direction[1])
                if next_position in visited:
                    continue

                if self.out_of_bounds(next_position):
                    region.perimeter += 1
                    continue

                next_idx = self.field_map[next_position[0]][next_position[1]]
                if next_idx == idx:
                    queue.add(next_position)
                    region.positions.add(next_position)
                else:
                    region.perimeter += 1

        self.remaining.difference_update(region.positions)
        self.regions.append(region)

    def neighbourhood(self, position: tuple[int, int]) -> list[list[int]]:
        neighbourhood = [[0] * CELL_SIZE for _ in range(CELL_SIZE)]
        idx = self.field_map[position[0]][position[1]]

        for row_index in range(CELL_SIZE):
            for col_index in range(CELL_SIZE):
                row, col = position[0] - 1 + row_index, position[1] - 1 + col_index
                if self.out_of_bounds((row, col)):
                    continue
                neighbourhood[row_index][col_index] = int(self.field_map[row][col] == idx)

        return neighbourhood

    def _count_corners(self, neighbourhood: list[list[int]]) -> int:
        return sum(1 for pattern in CORNER_PATTERNS if pattern(neighbourhood))

    def count_corners(self, position: tuple[int, int]) -> int:
        return self._count_corners(self.neighbourhood(position))

    def out_of_bounds(self, position: tuple[int, int]) -> bool:
        return not (0 <= position[0] < self._rows and 0 <= position[1] < self._cols)

    def price(self) -> int:
        return sum(region.price() for region in self.regions)

    def bulk_price(self) -> int:
        return sum(region.side_price() for region in self.regions)


def main(file_name: str = "input.txt") -> None:
    try:
        with open(file_name, 'r') as file:
            field_map = file.read().strip().split("\n")
        field = Field(field_map)

        print(f"The total price of the field is {field.price()}")
        print(f"With the bulk discount, the price is {field.bulk_price()}")

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    main(file_name)
