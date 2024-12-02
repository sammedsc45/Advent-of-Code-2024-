def is_safe(report):
    """Checks if a report is safe based on the given criteria."""
    n = len(report)
    if n < 2:
        return True

    increasing = report[1] > report[0]

    for i in range(1, n):
        diff = report[i] - report[i - 1]
        if not (1 <= abs(diff) <= 3):
            return False
        if (increasing and diff < 0) or (not increasing and diff > 0):
            return False
    return True

'''
[TASK-1]
def count_safe_reports(filename):
    """Counts the number of safe reports in a file.

    Args:
        filename: The name of the file containing the reports.

    Returns:
        The number of safe reports.
    """
    safe_count = 0
    try:
        with open(filename, 'r') as f:
            for line in f:
                report = list(map(int, line.strip().split()))
                if is_safe(report):
                    safe_count += 1
        return safe_count
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
'''

# [TASK 2]
def count_safe_reports_with_dampener(filename):
    """Counts safe reports, considering the Problem Dampener."""

    safe_count = 0
    try:
        with open(filename, 'r') as f:
            for line in f:
                report = list(map(int, line.strip().split()))

                if is_safe(report):
                    safe_count += 1
                    continue  # Already safe, no need to check further

                # Check if removing one level makes it safe
                for i in range(len(report)):
                    modified_report = report[:i] + report[i+1:]
                    if is_safe(modified_report):
                        safe_count += 1
                        break  # Found a way to make it safe

        return safe_count
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None


# Example usage:
filename = "input.txt"  # Replace with your filename
safe_reports_count = count_safe_reports_with_dampener(filename)

if safe_reports_count is not None:
    print(f"Number of safe reports (with dampener): {safe_reports_count}")