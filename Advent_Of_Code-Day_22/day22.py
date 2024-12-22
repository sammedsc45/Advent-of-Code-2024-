def parse_input(file_name):
    """Parse input from file"""
    with open(file_name, 'r') as f:
        return [int(line.strip()) for line in f.readlines()]


def next_number(n):
    """Calculate the next number in the sequence"""
    n ^= n << 6
    n &= 0xFFFFFF

    n ^= n >> 5
    n &= 0xFFFFFF

    n ^= n << 11
    n &= 0xFFFFFF

    return n


def part1(input_numbers):
    """Part 1: Sum of 2000th numbers"""
    total = 0
    for number in input_numbers:
        for _ in range(2000):
            number = next_number(number)
        total += number
    return total


def part2(input_numbers):
    """Part 2: Maximum bananas earned"""
    result = [0] * 130321
    seen = [float('inf')] * 130321

    def to_index(prev, curr):
        return 9 + curr % 10 - prev % 10

    for id, num in enumerate(input_numbers):
        zeroth = num
        first = next_number(zeroth)
        second = next_number(first)
        third = next_number(second)

        a, b, c, d = (0, to_index(zeroth, first), to_index(first, second), to_index(second, third))
        curr_num = third

        for _ in range(1997):
            prev_num = curr_num
            curr_num = next_number(curr_num)

            a, b, c, d = (b, c, d, to_index(prev_num, curr_num))

            key = 6859 * a + 361 * b + 19 * c + d

            if seen[key]!= id:
                result[key] += curr_num % 10
                seen[key] = id

    return max(result)


# Load input from file
input_numbers = parse_input('input.txt')

# Part 1
print(f"Part 1: {part1(input_numbers)}")

# Part 2
print(f"Part 2: {part2(input_numbers)}")
