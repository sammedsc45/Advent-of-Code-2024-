import sys
from itertools import product

# Constant for standard 4-directional movement
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    """
    Add two coordinate tuples together.

    Args:
        duple_1 (tuple): First coordinate tuple
        duple_2 (tuple): Second coordinate tuple

    Returns:
        tuple: Summed coordinate tuple
    """
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


class Region:
    """
    Represents a region in the garden plot map.

    Attributes:
        idx (str): Identifier for the plant type
        positions (set): Coordinates of plots in the region
        perimeter (int): Number of exposed sides
        corners (int): Number of unique corner points
    """

    def __init__(self, idx: str, start_position: tuple[int, int]) -> None:
        """
        Initialize a new region.

        Args:
            idx (str): Plant type identifier
            start_position (tuple): Starting coordinate
        """
        self.positions = {start_position}
        self.perimeter = 0
        self.corners = 0
        self.idx = idx

    def price(self) -> int:
        """
        Calculate price for Part 1 (area * perimeter).

        Returns:
            int: Total price of the region
        """
        return len(self.positions) * self.perimeter

    def side_price(self) -> int:
        """
        Calculate price for Part 2 (area * number of sides/corners).

        Returns:
            int: Total price of the region
        """
        return len(self.positions) * self.corners

    def __repr__(self) -> str:
        """
        String representation of the region.

        Returns:
            str: Description of the region
        """
        return f"Region {self.idx} in positions {self.positions}"


class Field:
    """
    Represents the entire garden plot field.

    Attributes:
        field_map (list): 2D map of garden plots
        regions (list): Detected regions in the field
    """

    def __init__(self, field_map: list[str]) -> None:
        """
        Initialize the field and detect regions.

        Args:
            field_map (list): 2D map of garden plots
        """
        self.field_map = field_map
        self.regions = []
        self.remaining = set(
            product(*[range(len(field_map)), range(len(field_map[0]))])
        )

        # Detect all regions
        while self.remaining:
            self.fill_region()

    def fill_region(self) -> None:
        """
        Detect and fill a single region in the field.
        """
        # Start from an unvisited position
        position = self.remaining.pop()
        queue = {position}
        visited = set()

        # Get plant type for this region
        idx = self.field_map[position[0]][position[1]]
        region = Region(idx, position)

        while queue:
            position = queue.pop()
            visited.add(position)

            # Count corners for this position
            region.corners += self.count_corners(position)

            # Explore adjacent positions
            for direction in DIRECTIONS:
                next_position = sum_duples(position, direction)

                # Skip already visited positions
                if next_position in visited:
                    continue

                # Check if out of bounds
                if self.out_of_bounds(next_position):
                    region.perimeter += 1
                    continue

                # Check adjacent position's plant type
                next_idx = self.field_map[next_position[0]][next_position[1]]
                if next_idx == idx:
                    queue.add(next_position)
                    region.positions.add(next_position)
                else:
                    region.perimeter += 1

        # Update remaining positions and add region
        self.remaining.difference_update(region.positions)
        self.regions.append(region)

    def neighbourhood(self, position: tuple[int, int]) -> list[list[int]]:
        """
        Generate a 3x3 neighborhood grid around a position.

        Args:
            position (tuple): Central position

        Returns:
            list: 3x3 grid representing neighborhood
        """
        neighbourhood = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        idx = self.field_map[position[0]][position[1]]

        for row_index in range(3):
            for col_index in range(3):
                row_position = position[0] - 1 + row_index
                col_position = position[1] - 1 + col_index

                # Skip out of bounds positions
                if self.out_of_bounds((row_position, col_position)):
                    continue

                next_idx = self.field_map[row_position][col_position]
                if next_idx == idx:
                    neighbourhood[row_index][col_index] = 1

        return neighbourhood

    def count_corners(self, position: tuple[int, int]) -> int:
        """
        Count unique corner points around a position.

        Args:
            position (tuple): Position to check

        Returns:
            int: Number of corner points
        """
        neighbourhood = self.neighbourhood(position)
        count = 0

        # Check 8 potential corner configurations
        corner_patterns = [
            (lambda n: n[1][0] == 0 and n[0][1] == 0),
            (lambda n: n[0][0] == 0 and n[1][0] == 1 and n[0][1] == 1),
            (lambda n: n[1][2] == 0 and n[0][1] == 0),
            (lambda n: n[0][2] == 0 and n[1][2] == 1 and n[0][1] == 1),
            (lambda n: n[1][0] == 0 and n[2][1] == 0),
            (lambda n: n[2][0] == 0 and n[1][0] == 1 and n[2][1] == 1),
            (lambda n: n[1][2] == 0 and n[2][1] == 0),
            (lambda n: n[2][2] == 0 and n[1][2] == 1 and n[2][1] == 1)
        ]

        # Count corners matching the patterns
        count = sum(1 for pattern in corner_patterns if pattern(neighbourhood))
        return count

    def out_of_bounds(self, position: tuple[int, int]) -> bool:
        """
        Check if a position is outside the field boundaries.

        Args:
            position (tuple): Position to check

        Returns:
            bool: True if out of bounds, False otherwise
        """
        return not (0 <= position[0] < len(self.field_map) and
                    0 <= position[1] < len(self.field_map[0]))

    def price(self) -> int:
        """
        Calculate total price for Part 1 (area * perimeter).

        Returns:
            int: Total price of all regions
        """
        return sum(region.price() for region in self.regions)

    def bulk_price(self) -> int:
        """
        Calculate total price for Part 2 (area * corners).

        Returns:
            int: Total price with bulk discount
        """
        return sum(region.side_price() for region in self.regions)


def main(file_name: str = "input.txt") -> None:
    """
    Main function to process the garden plot map.

    Args:
        file_name (str): Path to input file
    """
    try:
        # Read input file
        with open(file_name, 'r') as file:
            field_map = file.read().strip().split("\n")

        # Process the field
        field = Field(field_map)

        # Calculate and print prices
        price = field.price()
        print(f"The total price of the field is {price}")

        bulk_price = field.bulk_price()
        print(f"With the bulk discount, the price is {bulk_price}")

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    # Use command-line argument or default to input.txt
    file_name = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    main(file_name)