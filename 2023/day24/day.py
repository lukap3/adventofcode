# Advent of Code 2023 - Day 24

import sympy
from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day24/example.txt": [2, 47]}
    data_file = "2023/day24/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i, line in enumerate(data):
            position, velocity = line.split(" @ ")
            position = [int(p) for p in position.split(", ")]
            velocity = [int(v) for v in velocity.split(", ")]
            data[i] = (position, velocity)
        return data

    @classmethod
    def paths_collide(cls, line1, line2):
        (p1x, p1y, p1z), (v1x, v1y, v2z) = line1
        (p2x, p2y, p2z), (v2x, v2y, v2z) = line2

        try:
            t2 = (v1x * (p1y - p2y) + v1y * (p2x - p1x)) / (v1x * v2y - v1y * v2x)
            t1 = (p2x - p1x + v2x * t2) / v1x
        except ZeroDivisionError:
            return False, (0, 0)

        if t1 < 0 or t2 < 0:
            return False, (0, 0)
        else:
            return True, (p1x + (v1x * t1), p1y + (v1y * t1))

    def part_1_logic(self, hailstones):
        area_min, area_max = (200000000000000, 400000000000000)
        if len(hailstones) == 5:
            area_min, area_max = (7, 27)
        count = 0
        for i, hailstone1 in enumerate(hailstones[:-1]):
            for hailstone2 in hailstones[i:]:
                ok, (intersect_x, intersect_y) = self.paths_collide(
                    hailstone1, hailstone2
                )
                if (
                    ok
                    and area_min <= intersect_x < area_max
                    and area_min <= intersect_y <= area_max
                ):
                    count += 1
        return count

    @classmethod
    def find_intersections(cls, hailstones):
        lines = []
        t1, t2, t3 = sympy.symbols("t1 t2 t3")
        rock_px, rock_py, rock_pz = sympy.symbols("rock_px rock_py rock_pz")
        rock_vs = sympy.symbols("rock_vx rock_vy rock_vz")
        rock_ps = [rock_px, rock_py, rock_pz]

        for t, hailstone in zip((t1, t2, t3), hailstones):
            ps, vs = hailstone
            for rock_p, rock_v, p, v in zip(rock_ps, rock_vs, ps, vs):
                lines.append(sympy.Eq(rock_p + (rock_v * t), p + (v * t)))
        results = sympy.solve(lines)
        if len(results) != 1:
            raise Exception("No results or too many results")
        result = results[0]
        return result[rock_px], result[rock_py], result[rock_pz]

    def part_2_logic(self, hailstones):
        rock_position = self.find_intersections(hailstones[:3])
        return sum(rock_position)


Day()
