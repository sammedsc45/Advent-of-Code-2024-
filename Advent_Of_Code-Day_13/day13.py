import re


def calc_linear_combination(px, py, ax, ay, bx, by):
    """
    Calculate the minimal token cost for a linear combination of A and B presses.

    Returns:
        int: Minimal token cost (0 if no solution exists)
    """
    det = ax * by - ay * bx
    if det == 0:
        return 0

    num_a = px * by - py * bx
    num_b = py * ax - px * ay

    # Check if integer solution exists
    if num_a % det != 0 or num_b % det != 0:
        return 0

    a = num_a // det
    b = num_b // det

    if a >= 0 and b >= 0:
        return 3 * a + b
    return 0


def main():
    with open("input.txt", "r") as f:
        input_text = f.read()

    pattern = r"Button A: X\+(\d+), Y\+(\d+)\s+Button B: X\+(\d+), Y\+(\d+)\s+Prize: X=(\d+), Y=(\d+)"
    regex = re.compile(pattern)

    part_1 = 0
    part_2 = 0

    # Iterate over matches and extract data
    for match in regex.finditer(input_text):
        ax, ay, bx, by, px, py = map(int, match.groups())

        part_1 += calc_linear_combination(px, py, ax, ay, bx, by)
        part_2 += calc_linear_combination(px + 10000000000000, py + 10000000000000, ax, ay, bx, by)

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")


if __name__ == "__main__":
    main()
