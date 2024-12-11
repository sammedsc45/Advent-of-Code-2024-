from collections import defaultdict

def solve_plutonian_pebbles_optimized(filename, num_blinks):
    """Simulates Plutonian pebble evolution (optimized for many blinks)."""
    try:
        with open(filename, 'r') as f:
            initial_stones = [int(s) for s in f.read().strip().split()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

    stone_counts = defaultdict(int)
    for stone in initial_stones:
        stone_counts[stone] += 1

    for _ in range(num_blinks):
        new_stone_counts = defaultdict(int)
        for stone, count in stone_counts.items():
            if stone == 0:
                new_stone_counts[1] += count
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                mid = len(s) // 2
                new_stone_counts[int(s[:mid])] += count
                new_stone_counts[int(s[mid:])] += count
            else:
                new_stone_counts[stone * 2024] += count
        stone_counts = new_stone_counts

    total_stones = sum(stone_counts.values())
    return total_stones

# Example usage:
filename = "input.txt"

num_stones_25_blinks = solve_plutonian_pebbles_optimized(filename, 25)
num_stones_75_blinks = solve_plutonian_pebbles_optimized(filename, 75)
if num_stones_25_blinks is not None:
    print(f"Number of stones after 25 blinks: {num_stones_25_blinks}")
if num_stones_75_blinks is not None:
    print(f"Number of stones after 75 blinks: {num_stones_75_blinks}")