''' [Task-01]
def count_xmas(filename):
    """Counts the occurrences of "XMAS" (and its reverse) in a word search grid.

    Args:
        filename: The path to the input file containing the word search grid.

    Returns:
        The number of times "XMAS" appears in the grid, or None if the file
        is not found.
    """
    try:
        with open(filename, 'r') as f:
            grid = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

    rows = len(grid)
    cols = len(grid[0])
    count = 0

    for r in range(rows):
        for c in range(cols):
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue  # Skip no movement

                    word = ""
                    for i in range(4):  # "XMAS" has length 4
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < rows and 0 <= nc < cols:
                            word += grid[nr][nc]
                        else:
                            break  # Out of bounds

                    if word == "XMAS":  # Only count "XMAS" once
                        count += 1

    return count
'''

# [Task-02]
def count_x_mas(filename):
    """Counts non-overlapping X-MAS patterns in a grid."""
    try:
        with open(filename, 'r') as f:
            grid = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

    rows = len(grid)
    cols = len(grid[0])
    count = 0
    used = set()  # Keep track of used center 'A's

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if (r, c) in used:  # Skip if center 'A' already used
                continue
            if grid[r][c] != 'A':
                continue

            found = False
            for mas1_rev in [False, True]:
                for mas2_rev in [False, True]:
                    mas1 = ""
                    mas2 = ""

                    chars1 = [grid[r - 1][c - 1], grid[r][c], grid[r + 1][c + 1]]
                    if mas1_rev:
                        chars1.reverse()
                    mas1 = "".join(chars1)

                    chars2 = [grid[r - 1][c + 1], grid[r][c], grid[r + 1][c - 1]]
                    if mas2_rev:
                        chars2.reverse()
                    mas2 = "".join(chars2)

                    if mas1 in ("MAS", "SAM") and mas2 in ("MAS", "SAM"):
                        count += 1
                        used.add((r,c)) # this 'A' is middle char for X-MAS and mark it as used
                        found = True
                        break # only count one for a given center
                if found:
                    break

    return count


# Example usage
filename = "input.txt"
xmas_count = count_x_mas(filename)
if xmas_count is not None:
    print(f"XMAS appears {xmas_count} times.")