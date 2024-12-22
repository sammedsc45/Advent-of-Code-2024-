from time import perf_counter
from collections import Counter

timer_script_start = perf_counter()
INPUT_PATH = "input.txt"

timer_parse_start = perf_counter()
with open(INPUT_PATH) as file:
    lines = file.read().splitlines()

def get_pad(pad_lines):
    pad = {(i, j): c for i, line in enumerate(pad_lines) for j, c in enumerate(line) if c != "."}
    pad.update({v: k for k, v in pad.items()})
    return pad

num_pad = get_pad(["789", "456", "123", ".0A"])
dir_pad = get_pad([".^A", "<v>"])

timer_parse_end = timer_part1_start = perf_counter()

def step(source, target, pad):
    ti, tj = pad[target]
    si, sj = pad[source]
    di = ti - si
    dj = tj - sj
    vert = "v"*di+"^"*-di
    horiz = ">"*dj+"<"*-dj
    if dj > 0 and (ti,sj) in pad:
        return vert+horiz+"A"
    if (si,tj) in pad:
        return horiz+vert+"A"
    if (ti,sj) in pad:
        return vert+horiz+"A"

def get_routes(path, pad):
    start = "A"
    out = []
    for end in path:
        out.append(step(start,end,pad))
        start = end
    return "".join(out)

num_routes = [get_routes(line, num_pad) for line in lines]
rad_routes = [get_routes(route, dir_pad) for route in num_routes]
cold_routes = [get_routes(route, dir_pad) for route in rad_routes]
p1 = sum(len(route) * int(line[:-1]) for route, line in zip(cold_routes, lines))
print("Part 1:", p1)
timer_part1_end = timer_part2_start = perf_counter()


def get_routes2(path, pad):
    start = "A"
    out = []
    for end in path:
        out.append(step(start, end, pad))
        start = end
    return Counter(out)


def route_len(route):
    return sum(len(k) * v for k, v in route.items())


robot_routes = [Counter([route]) for route in num_routes]
for _ in range(25):
    new_routes = []
    for route_counter in robot_routes:
        new_route = Counter()
        for sub_route, qty in route_counter.items():
            new_counts = get_routes2(sub_route, dir_pad)
            for k in new_counts:
                new_counts[k] *= qty
            new_route.update(new_counts)
        new_routes.append(new_route)
    robot_routes = new_routes

p2 = sum(route_len(route) * int(line[:-1]) for route, line in zip(robot_routes, lines))
print("Part 2:", p2)
timer_part2_end = timer_script_end = perf_counter()