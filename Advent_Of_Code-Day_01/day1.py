from collections import Counter

def read_lists_from_file(filename):
    """
    Reads pairs of numbers from a file and returns two separate lists.

    Args:
        filename (str): The name of the file containing the number pairs.

    Returns:
        tuple: Two lists of numbers (left_list, right_list)
    """
    left_list, right_list = [], []

    try:
        with open(filename, 'r') as file:
            for line in file:
                try:
                    left, right = map(int, line.strip().split())
                    left_list.append(left)
                    right_list.append(right)
                except ValueError:
                    print(f"Skipping invalid line: {line.strip()}")
        return left_list, right_list
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

def calculate_total_distance(left_list, right_list):
    """
    Calculates the total distance between two sorted lists of numbers.

    Args:
        left_list (list): A sorted list of numbers.
        right_list (list): A sorted list of numbers.

    Returns:
        int: The total distance between the two lists.
    """
    if len(left_list)!= len(right_list):
        raise ValueError("Lists must be of equal length")

    left_list.sort()
    right_list.sort()
    return sum(abs(left - right) for left, right in zip(left_list, right_list))

def calculate_similarity_score(left_list, right_list):
    """
    Calculates the similarity score between two lists based on weighted overlaps.

    Args:
        left_list (list): The first list of numbers.
        right_list (list): The second list of numbers.

    Returns:
        int: The similarity score.
    """
    right_counts = Counter(right_list)
    return sum(num * right_counts[num] for num in left_list)

def process_file(filename):
    """
    Orchestrates the file reading, calculation, and printing of both distance and similarity score.

    Args:
        filename (str): The name of the file containing the number pairs.
    """
    lists = read_lists_from_file(filename)
    if lists is None:
        return

    left_list, right_list = lists
    total_distance = calculate_total_distance(left_list[:], right_list[:])  # Create copies for sorting
    similarity_score = calculate_similarity_score(left_list, right_list)

    print("-----------------------------------")
    print(f"Total Distance: {total_distance}")
    print(f"Similarity Score: {similarity_score}")
    print("-----------------------------------")

filename = "input.txt"  # Replace with your filename
process_file(filename)
