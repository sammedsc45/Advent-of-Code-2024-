from collections import defaultdict, deque

def process_input(filename):
    """Reads and processes rules and updates efficiently."""
    rules = defaultdict(list)
    updates = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                if '|' in line:
                    before, after = map(int, line.split('|'))
                    rules[before].append(after)
                else:
                    updates.append(list(map(int, line.split(','))))
    return rules, updates


def is_update_ordered(update, rules):
    """Checks update order using a set for seen pages."""
    seen = set()
    for page in update:
        for prev in seen:
            if page not in rules.get(prev, []):
                return False
        seen.add(page)
    return True


def topological_sort(update, rules):
    """Reorders an update based on the given rules."""
    in_degree = {page: 0 for page in update}
    graph = {page: [] for page in update}

    for before, afters in rules.items():
        if before in update:
            for after in afters:
                if after in update:
                    graph[before].append(after)
                    in_degree[after] += 1

    # Perform topological sort
    queue = deque([node for node in update if in_degree[node] == 0])
    sorted_order = []

    while queue:
        current = queue.popleft()
        sorted_order.append(current)

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_order


def calculate_middle_pages(updates, rules):
    """Calculates the middle pages for ordered and reordered updates."""
    correctly_ordered_sum = 0
    reordered_sum = 0

    for update in updates:
        if is_update_ordered(update, rules):
            # Correctly ordered: take the middle page
            correctly_ordered_sum += update[(len(update) + 1) // 2 - 1]
        else:
            # Not ordered: reorder and take the middle page
            sorted_update = topological_sort(update, rules)
            reordered_sum += sorted_update[(len(sorted_update) + 1) // 2 - 1]

    return correctly_ordered_sum, reordered_sum


# Main logic
rules, updates = process_input('input.txt')

# Calculate results
correct_sum, reorder_sum = calculate_middle_pages(updates, rules)

# Output
print("Sum of Middle Pages for Correctly Ordered Updates:", correct_sum)
print("Sum of Middle Pages After Reordering Incorrect Updates:", reorder_sum)
