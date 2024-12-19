def can_form_design(design, patterns):
    n = len(design)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(n):
        if dp[i]:
            for pattern in patterns:
                pat_len = len(pattern)
                if i + pat_len <= n and design[i:i + pat_len] == pattern:
                    dp[i + pat_len] = True
    return dp[n]


def count_ways(design, patterns):
    n = len(design)
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(n):
        if dp[i]:
            for pattern in patterns:
                pat_len = len(pattern)
                if i + pat_len <= n and design[i:i + pat_len] == pattern:
                    dp[i + pat_len] += dp[i]
    return dp[n]


def main():
    with open('input.txt', 'r') as f:
        data = f.read().splitlines()

    # Find the blank line index
    blank_line_index = -1
    for i, line in enumerate(data):
        if not line:
            blank_line_index = i
            break

    # Extract patterns and designs
    patterns = data[0].split(', ')
    designs = data[blank_line_index + 1:]

    # Part 1: Count the number of possible designs
    possible_count = 0
    total_ways = 0
    for design in designs:
        if can_form_design(design, patterns):
            possible_count += 1
            total_ways += count_ways(design, patterns)

    # Output results
    print("Part 1:", possible_count)
    print("Part 2:", total_ways)


if __name__ == "__main__":
    main()
