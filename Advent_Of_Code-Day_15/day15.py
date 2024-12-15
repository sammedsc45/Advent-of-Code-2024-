def read_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip('\n').split('\n\n')
    return data


def parse_warehouse_and_instructions(data):
    warehouse_str, instructions_str = data
    warehouse = [list(row) for row in warehouse_str.split('\n')]
    instructions = instructions_str.replace('\n', '')
    return warehouse, instructions


def simulate_robot_movement(warehouse, instructions):
    directions = {'v': (1, 0), '<': (0, -1), '>': (0, 1), '^': (-1, 0)}
    robot_pos = [(i, j) for i, row in enumerate(warehouse)
                 for j, cell in enumerate(row) if cell == '@'][0]

    for instruction in instructions:
        dx, dy = directions[instruction]
        nx, ny = robot_pos[0] + dx, robot_pos[1] + dy

        if warehouse[nx][ny] == '.':
            warehouse[robot_pos[0]][robot_pos[1]] = '.'
            warehouse[nx][ny] = '@'
            robot_pos = (nx, ny)
            continue

        if warehouse[nx][ny] == '#':
            continue

        tx, ty = nx, ny
        while warehouse[tx][ty] == 'O':
            tx, ty = tx + dx, ty + dy

        if warehouse[tx][ty] == '#':
            continue

        warehouse[tx][ty] = 'O'
        warehouse[nx][ny] = '@'
        warehouse[robot_pos[0]][robot_pos[1]] = '.'
        robot_pos = (nx, ny)

    return warehouse


def calculate_gps_sum(warehouse):
    gps_sum = 0
    for i, row in enumerate(warehouse):
        for j, cell in enumerate(row):
            if cell == 'O':
                gps_sum += 100 * i + j
    return gps_sum


def expand_warehouse(warehouse):
    expanded = []
    for row in warehouse:
        expanded_row = []
        for cell in row:
            if cell == '#':
                expanded_row.extend(['#', '#'])
            elif cell == 'O':
                expanded_row.extend(['[', ']'])
            elif cell == '.':
                expanded_row.extend(['.', '.'])
            elif cell == '@':
                expanded_row.extend(['@', '.'])
        expanded.append(expanded_row)
    return expanded


def simulate_wide_robot_movement(wide_warehouse, instructions):
    directions = {'v': (1, 0), '<': (0, -1), '>': (0, 1), '^': (-1, 0)}
    robot_pos = [(i, j) for i, row in enumerate(wide_warehouse)
                 for j, cell in enumerate(row) if cell == '@'][0]

    for instruction in instructions:
        dx, dy = directions[instruction]
        nx, ny = robot_pos[0] + dx, robot_pos[1] + dy

        if wide_warehouse[nx][ny] == '.':
            wide_warehouse[robot_pos[0]][robot_pos[1]] = '.'
            wide_warehouse[nx][ny] = '@'
            robot_pos = (nx, ny)
            continue

        if wide_warehouse[nx][ny] == '#':
            continue

        if dx == 0:
            tx, ty = nx, ny
            dist = 0
            while wide_warehouse[tx][ty] in ['[', ']']:
                dist += 1
                tx, ty = tx + dx, ty + dy
            if wide_warehouse[tx][ty] == '#':
                continue
            for i in range(dist):
                wide_warehouse[tx][ty] = wide_warehouse[tx - dx][ty - dy]
                tx, ty = tx - dx, ty - dy
            wide_warehouse[nx][ny] = '@'
            wide_warehouse[robot_pos[0]][robot_pos[1]] = '.'
            robot_pos = (nx, ny)
            continue

        to_push = [{(robot_pos[0], robot_pos[1])}]
        no_wall = True
        all_empty = False
        while no_wall and not all_empty:
            next_push = set()
            all_empty = True
            for cx, cy in to_push[-1]:
                if wide_warehouse[cx][cy] == '.':
                    continue
                tx, ty = cx + dx, cy + dy
                if wide_warehouse[tx][ty] != '.':
                    all_empty = False
                next_push.add((tx, ty))
                if wide_warehouse[tx][ty] == '#':
                    no_wall = False
                    break
                elif wide_warehouse[tx][ty] == '[':
                    next_push.add((tx, ty + 1))
                elif wide_warehouse[tx][ty] == ']':
                    next_push.add((tx, ty - 1))
            to_push.append(next_push)

        if not no_wall:
            continue

        for i in range(len(to_push) - 1, 0, -1):
            for cx, cy in to_push[i]:
                fx, fy = cx - dx, cy - dy
                if (fx, fy) in to_push[i - 1]:
                    wide_warehouse[cx][cy] = wide_warehouse[fx][fy]
                else:
                    wide_warehouse[cx][cy] = '.'

        wide_warehouse[robot_pos[0]][robot_pos[1]] = '.'
        robot_pos = (nx, ny)

    return wide_warehouse


def calculate_wide_gps_sum(wide_warehouse):
    gps_sum = 0
    for i, row in enumerate(wide_warehouse):
        for j, cell in enumerate(row):
            if cell == '[':
                gps_sum += 100 * i + j
    return gps_sum


def solve_part1(input_file):
    data = read_input(input_file)
    warehouse, instructions = parse_warehouse_and_instructions(data)
    final_warehouse = simulate_robot_movement(warehouse, instructions)
    return calculate_gps_sum(final_warehouse)


def solve_part2(input_file):
    data = read_input(input_file)
    warehouse, instructions = parse_warehouse_and_instructions(data)
    wide_warehouse = expand_warehouse(warehouse)
    final_wide_warehouse = simulate_wide_robot_movement(wide_warehouse, instructions)
    return calculate_wide_gps_sum(final_wide_warehouse)


input_file = "input.txt"
part1_answer = solve_part1(input_file)
part2_answer = solve_part2(input_file)

print(f"Part 1 answer: {part1_answer}")
print(f"Part 2 answer: {part2_answer}")