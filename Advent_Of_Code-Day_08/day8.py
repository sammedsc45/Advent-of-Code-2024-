def load_antenna_grid_and_locations(document_path: str) -> tuple[list[str], dict[str, list[tuple[int, int]]]]:
    """Load grid and antenna locations from file"""
    with open(document_path, 'r') as file:
        grid = file.read().splitlines()
    antenna_locations: dict[str, list[tuple[int, int]]] = {}
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char!= ".":
                antenna_locations.setdefault(char, []).append((r, c))
    return grid, antenna_locations


def get_anti_node_pairs_from_antennae(n1: tuple[int, int], n2: tuple[int, int]) -> list[tuple[int, int]]:
    """Calculate anti-node pairs from two antennae"""
    return [(n2[0] + (n2[0] - n1[0]), n2[1] + (n2[1] - n1[1])),
            (n1[0] - (n2[0] - n1[0]), n1[1] - (n2[1] - n1[1]))]


def get_all_anti_node_pairs(
    grid: list[str], antenna_locations: dict[str, list[tuple[int, int]]]
) -> set[tuple[int, int]]:
    """Get all anti-node pairs from antenna locations"""
    anti_nodes: set[tuple[int, int]] = set()
    for nodes in antenna_locations.values():
        if len(nodes) > 1:
            anti_nodes.update(
                (n2[0] + (n2[0] - n1[0]), n2[1] + (n2[1] - n1[1]))
                for k, n1 in enumerate(nodes)
                for n2 in nodes[k + 1:]
                if (0 <= n2[0] + (n2[0] - n1[0]) <= len(grid) - 1) and
                   (0 <= n2[1] + (n2[1] - n1[1]) <= len(grid[0]) - 1)
            )
    return anti_nodes


class AffineEq:
    """Affine Equation (AX + BY + C = 0)"""
    def __init__(self, n1: tuple[int, int], n2: tuple[int, int]):
        self.slope_x = n1[0] - n2[0]
        self.slope_y = n2[1] - n1[1]
        self.offset = -n1[1] * self.slope_x - n1[0] * self.slope_y

    def on_line(self, coord: tuple[int, int]) -> bool:
        """Check if point is on the line"""
        return self.slope_x * coord[1] + self.slope_y * coord[0] + self.offset == 0


def get_all_anti_nodes(grid: list[str], antenna_locations: dict[str, list[tuple[int, int]]]) -> list[tuple[int, int]]:
    """Get all anti-nodes from grid and antenna locations"""
    equations = [AffineEq(n1, n2)
                 for nodes in antenna_locations.values()
                 if len(nodes) > 1
                 for k, n1 in enumerate(nodes)
                 for n2 in nodes[k + 1:]]
    anti_nodes = [(r, c)
                  for r in range(len(grid))
                  for c in range(len(grid[0]))
                  if any(eq.on_line((r, c)) for eq in equations)]
    return anti_nodes


# Main
grid, locations = load_antenna_grid_and_locations("input.txt")
anti_node_pairs = get_all_anti_node_pairs(grid, locations)
anti_nodes = get_all_anti_nodes(grid, locations)
print(f"Part 1: {len(anti_node_pairs)}")
print(f"Part 2: {len(anti_nodes)}")
