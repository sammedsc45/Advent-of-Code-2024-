from collections import defaultdict, deque

def solve_lan_party(filename):
    """Solves the LAN party problem, counting sets and finding the password."""

    try:
        with open(filename, 'r') as f:
            connections = [line.strip().split('-') for line in f]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, None

    graph = defaultdict(set)
    for a, b in connections:
        graph[a].add(b)
        graph[b].add(a)

    def is_clique(nodes, graph):
        """Checks if a set of nodes forms a clique."""
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if nodes[j] not in graph[nodes[i]]:
                    return False
        return True

    # Part 1 logic
    count_part1 = 0
    for node1 in graph:
        for node2 in graph[node1]:
            if node2 > node1:
                for node3 in graph[node2]:
                    if node3 > node2 and node3 in graph[node1]:
                        # Check if this is a valid set of 3 connected nodes
                        if node1 in graph[node3]:
                            # Check if the set includes a computer that starts with "t"
                            if any(node.startswith('t') for node in (node1, node2, node3)):
                                count_part1 += 1

    # Part 2 logic
    max_clique = []
    for node in graph:
        queue = deque([[node]])
        while queue:
            current_nodes = queue.popleft()
            if is_clique(current_nodes, graph):
                if len(current_nodes) > len(max_clique):
                    max_clique = current_nodes

                for next_node in sorted(graph[current_nodes[-1]]):
                    if next_node not in current_nodes and next_node > current_nodes[-1]:
                       queue.append(current_nodes + [next_node])

    max_clique.sort()
    password = ",".join(max_clique)

    return count_part1, password


# Example usage:
filename = "input.txt"
relevant_sets, lan_party_password = solve_lan_party(filename)

if relevant_sets is not None:
    print(f"Number of sets of three inter-connected computers with at least one t (Part 1): {relevant_sets}")

if lan_party_password is not None:
    print(f"The password for the LAN party (Part 2): {lan_party_password}")