import re
import math


class Robot:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


class Submap:
    def __init__(self, x_left, y_top, x_right, y_bot):
        self.x_left = x_left
        self.y_top = y_top
        self.x_right = x_right
        self.y_bot = y_bot


def parse_input(input_str):
    robots = []
    robot_pattern = re.compile(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')
    for line in input_str.splitlines():
        match = robot_pattern.match(line)
        if match:
            px, py, vx, vy = map(int, match.groups())
            robots.append(Robot(px, py, vx, vy))
    return robots


def move_robots(robots, grid_width, grid_height):
    for robot in robots:
        robot.x = (robot.x + robot.vx) % grid_width
        robot.y = (robot.y + robot.vy) % grid_height
    return robots


def get_quadrants(grid_width, grid_height):
    horiz_mid_left = (grid_width - 2) // 2
    horiz_mid_right = (grid_width + 2) // 2
    vert_mid_top = (grid_height - 2) // 2
    vert_mid_bot = (grid_height + 2) // 2

    return [
        Submap(0, 0, horiz_mid_left, vert_mid_top),
        Submap(horiz_mid_right, 0, grid_width - 1, vert_mid_top),
        Submap(0, vert_mid_bot, horiz_mid_left, grid_height - 1),
        Submap(horiz_mid_right, vert_mid_bot, grid_width - 1, grid_height - 1)
    ]


def robot_in_submap(robot, submap):
    return (submap.x_left <= robot.x <= submap.x_right and
            submap.y_top <= robot.y <= submap.y_bot)


def solve_part_1(robots, grid_width, grid_height):
    # Create a copy of robots to avoid modifying the original
    test_robots = [Robot(r.x, r.y, r.vx, r.vy) for r in robots]

    # Move robots for 100 seconds
    for _ in range(100):
        move_robots(test_robots, grid_width, grid_height)

    # Calculate safety factor
    quadrants = get_quadrants(grid_width, grid_height)
    quadrant_counts = [sum(1 for robot in test_robots if robot_in_submap(robot, q)) for q in quadrants]
    return math.prod(quadrant_counts)


def solve_part_2(robots, grid_width, grid_height):
    def is_easter_egg_moment(current_robots):
        center_x_start = grid_width // 4
        center_x_end = grid_width * 3 // 4
        center_y_start = grid_height // 4
        center_y_end = grid_height * 3 // 4

        center_robots = sum(1 for r in current_robots
                            if (center_x_start <= r.x <= center_x_end) and
                            (center_y_start <= r.y <= center_y_end))

        return center_robots > len(current_robots) // 2

    # Create a copy of robots to avoid modifying the original
    test_robots = [Robot(r.x, r.y, r.vx, r.vy) for r in robots]

    for seconds in range(10000):  # Reasonable upper limit
        if is_easter_egg_moment(test_robots):
            return seconds

        move_robots(test_robots, grid_width, grid_height)

    return -1  # If no Easter egg moment found


def main():
    # Read input from file
    with open('input.txt', 'r') as file:
        input_str = file.read().strip()

    # Parse input
    robots = parse_input(input_str)

    # Grid dimensions
    grid_width, grid_height = 101, 103

    # Solve Part 1
    part1_result = solve_part_1(robots, grid_width, grid_height)
    print(f"Part 1 Result (Safety Factor): {part1_result}")

    # Solve Part 2
    part2_result = solve_part_2(robots, grid_width, grid_height)
    print(f"Part 2 Result (Seconds to Easter Egg): {part2_result}")


if __name__ == "__main__":
    main()