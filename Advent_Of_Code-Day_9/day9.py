def solve(disk_map, part2=False):
    # Initialize data structures
    A = []  # File blocks
    SPACE = []  # Free space blocks
    FINAL = []  # Final disk layout
    file_id = 0
    pos = 0

    # Parse the input disk map
    for i, c in enumerate(disk_map):
        if i % 2 == 0:
            # File block
            if part2:
                A.append((pos, int(c), file_id))

            # Add file blocks to FINAL
            for _ in range(int(c)):
                FINAL.append(file_id)
                if not part2:
                    A.append((pos, 1, file_id))
                pos += 1

            file_id += 1
        else:
            # Free space block
            SPACE.append((pos, int(c)))
            for _ in range(int(c)):
                FINAL.append(None)
                pos += 1

    # Compact files
    for (pos, sz, file_id) in reversed(A):
        for space_i, (space_pos, space_sz) in enumerate(SPACE):
            # Find suitable free space
            if space_pos < pos and sz <= space_sz:
                # Move file block
                for i in range(sz):
                    assert FINAL[pos + i] == file_id, f'Unexpected file block at {pos + i}'
                    FINAL[pos + i] = None
                    FINAL[space_pos + i] = file_id

                # Update free space
                SPACE[space_i] = (space_pos + sz, space_sz - sz)
                break

    # Calculate checksum
    ans = sum(i * c for i, c in enumerate(FINAL) if c is not None)
    return ans


# Read input from file
with open('input.txt', 'r') as file:
    disk_map = file.read().strip()

# Calculate both parts
part1 = solve(disk_map, part2=False)
part2 = solve(disk_map, part2=True)

print(f"Part 1 Checksum: {part1}")
print(f"Part 2 Checksum: {part2}")