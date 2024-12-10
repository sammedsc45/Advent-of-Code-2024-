import re
'''[TASK-1]
def calculate_mul_sum(filename):
    """Calculates the sum of results from valid mul instructions in a file.

    Args:
        filename: The path to the input file.

    Returns:
        The sum of the multiplication results, or None if the file isn't found.
    """

    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

    mul_sum = 0
    for match in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", content):  # Optimized regex
        num1 = int(match.group(1))
        num2 = int(match.group(2))
        mul_sum += num1 * num2
    return mul_sum
'''
# TASK-2
def calculate_mul_sum_with_conditions(filename):
    """Calculates the sum of enabled mul instructions, considering do() and don't().

    Args:
        filename: The path to the input file.

    Returns:
        The sum of the multiplication results, or None if the file is not found.
    """

    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

    mul_sum = 0
    enabled = True  # mul instructions are initially enabled

    for match in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)", content):
        instruction = match.group(0)

        if instruction == "do()":
            enabled = True
        elif instruction == "don't()":
            enabled = False
        elif enabled:  # Only process mul if enabled
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            mul_sum += num1 * num2

    return mul_sum


# Example usage:
filename = "input.txt"  # Replace with your input file name
result = calculate_mul_sum_with_conditions(filename)

if result is not None:
    print(f"Sum of enabled multiplication results: {result}")