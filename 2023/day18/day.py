# Advent of Code 2023 - Day 18

from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day18/example.txt": [62, 952408144115]}
    data_file = "2023/day18/data.txt"

    d_map = {
        "R": lambda p, n: (p[0], p[1] + n),
        "L": lambda p, n: (p[0], p[1] - n),
        "U": lambda p, n: (p[0] - n, p[1]),
        "D": lambda p, n: (p[0] + n, p[1]),
    }

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        dirs = ["R", "D", "L", "U"]

        data_1 = []
        data_2 = []
        for i in range(len(data)):
            direction, steps, hex_num = data[i].split(" ")
            steps = int(steps)
            hex_num = hex_num[2:-1]
            steps_hex = int(hex_num[:5], 16)
            direction_hex = dirs[int(hex_num[5], 16)]
            data_1.append((direction, steps))
            data_2.append((direction_hex, steps_hex))
        return data_1, data_2

    @classmethod
    def calc_area(cls, corners, len_edges):
        n = len(corners)
        area = 0
        for i in range(n):
            x1, y1 = corners[i]
            x2, y2 = corners[(i + 1) % n]
            area += x1 * y2 - x2 * y1
        area = abs(area) // 2
        return (area - len_edges // 2 + 1) + len_edges

    @classmethod
    def get_corners_edges(cls, data):
        pos = (0, 0)
        corners = []
        len_edges = 0
        for direction, steps in data:
            pos = cls.d_map[direction](pos, steps)
            len_edges += steps
            corners.append(pos)
        return corners, len_edges

    def part_1_logic(self, data):
        corners, len_edges = self.get_corners_edges(data[0])
        return self.calc_area(corners, len_edges)

    def part_2_logic(self, data):
        corners, len_edges = self.get_corners_edges(data[1])
        return self.calc_area(corners, len_edges)


Day()
