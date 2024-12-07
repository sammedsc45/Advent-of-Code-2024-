def evaluate(nums, ops):
    """Evaluates an expression with +, *, and || operators (or only + and *)."""
    result = nums[0]
    for i in range(len(ops)):
        if ops[i] == '+':
            result += nums[i + 1]
        elif ops[i] == '*':
            result *= nums[i + 1]
        elif ops[i] == '||':
            result = int(str(result) + str(nums[i + 1]))
    return result


def solve_calibration(filename, include_concatenation=False):
    """Solves the calibration problem (Part One or Part Two)."""

    total_calibration_result = 0
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                test_value = int(parts[0])
                nums_str = parts[1].strip().split()
                nums = [int(num) for num in nums_str]

                num_ops = len(nums) - 1
                possible = False

                num_operators = 3 if include_concatenation else 2  # 2 for Part 1, 3 for Part 2
                for i in range(num_operators**num_ops):
                    ops = []
                    temp = i
                    for _ in range(num_ops):
                        op_code = temp % num_operators
                        if op_code == 0:
                            ops.append('+')
                        elif op_code == 1:
                            ops.append('*')
                        elif op_code == 2:  # Only for Part 2
                            ops.append('||')
                        temp //= num_operators

                    if evaluate(nums, ops) == test_value:
                        possible = True
                        break

                if possible:
                    total_calibration_result += test_value

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