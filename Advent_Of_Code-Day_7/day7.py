from itertools import product


def evaluate(nums, ops):
    """Evaluates an expression with +, *, and || operators (or only + and *)."""
    result = nums[0]
    for op, num in zip(ops, nums[1:]):
        if op == '+':
            result += num
        elif op == '*':
            result *= num
        elif op == '||':
            result = int(str(result) + str(num))
    return result


def solve_calibration(filename, include_concatenation=False):
    """Solves the calibration problem (Part One or Part Two)."""

    total_calibration_result = 0
    ops_set = ['+', '*'] if not include_concatenation else ['+', '*', '||']

    try:
        with open(filename, 'r') as f:
            for line in f:
                test_value, nums_str = line.strip().split(':')
                nums = [int(num) for num in nums_str.split()]

                # Use itertools.product for generating all possible operations combinations
                for ops in product(ops_set, repeat=len(nums) - 1):
                    if evaluate(nums, ops) == int(test_value):
                        total_calibration_result += int(test_value)
                        break  # Once we find a match, no need to continue checking for this line

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

    return total_calibration_result


# Example usage (for both parts):
filename = "input.txt"

# Part One
result_part_one = solve_calibration(filename)
if result_part_one is not None:
    print(f"Total calibration result (Part One): {result_part_one}")

# Part Two
result_part_two = solve_calibration(filename, include_concatenation=True)
if result_part_two is not None:
    print(f"Total calibration result (Part Two): {result_part_two}")