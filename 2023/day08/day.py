import math
from functools import reduce

from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {
        "2023/day08/example.txt": [2, None],
        "2023/day08/example2.txt": [None, 6],
    }
    data_file = "2023/day08/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        directions = list(data[0])
        nodes = {}
        for line in data[2:]:
            line = line.split(" = ")
            left, right = line[1][1:-1].split(", ")
            nodes[line[0]] = (left, right)
        return directions, nodes

    @classmethod
    def get_cycle(cls, start, nodes, directions):
        ends = {node: [] for node in nodes if node.endswith("Z")}

        step = 0
        while True:
            direction = directions[step % len(directions)]
            start = nodes[start][0] if direction == "L" else nodes[start][1]
            step += 1

            if start.endswith("Z"):
                matching_steps = [
                    s
                    for s in ends[start]
                    if s % len(directions) == step % len(directions)
                ]
                if matching_steps:
                    return matching_steps[-1]
                ends[start].append(step)

    def part_1_logic(self, data):
        directions, nodes = data
        # don't run for part 2 inputs
        if "AAA" not in nodes:
            return None
        step = 0
        start = "AAA"
        while start != "ZZZ":
            direction = directions[step % len(directions)]
            start = nodes[start][0] if direction == "L" else nodes[start][1]
            step += 1
        return step

    def part_2_logic(self, data):
        directions, nodes = data
        starts = [node for node in nodes if node.endswith("A")]

        # don't run for part 1 inputs
        if len(starts) == 1:
            return None

        cycles = [self.get_cycle(start, nodes, directions) for start in starts]

        def lcm(a, b):
            return abs(a * b) // math.gcd(a, b)

        return reduce(lcm, cycles)


day = Day()
