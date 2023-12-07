import math
import re

from lib import AdventDay


class Day(AdventDay):
    test_files = {"2023/data/day06/example.txt": [288, 71503]}
    data_file = "2023/data/day06/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i in range(len(data)):
            data[i] = [int(m) for m in re.findall(r"\d+", data[i])]
        return [(data[0][i], data[1][i]) for i in range(len(data[0]))]

    @classmethod
    def find_bounds(cls, race_time, record):
        a = -1
        b = race_time
        c = -record

        # calculate the upper/lower bounds
        delta = b**2 - 4 * a * c
        root1 = (-b - math.sqrt(delta)) / (2 * a)
        root2 = (-b + math.sqrt(delta)) / (2 * a)
        lower_bound = int(min(root1, root2))
        upper_bound = int(max(root1, root2))

        # check the upper and lower bounds for rounding errors
        if not (race_time - lower_bound) * lower_bound > record:
            lower_bound += 1
        if not (race_time - upper_bound) * upper_bound > record:
            upper_bound -= 1

        return lower_bound, upper_bound

    def part_1_logic(self, data):
        ret = 1
        for race in data:
            race_time, record = race
            min_hold, max_hold = self.find_bounds(race_time, record)
            wins = int(max_hold) - int(min_hold) + 1
            ret *= wins
        return ret

    def part_2_logic(self, data):
        race_time = int("".join(map(str, [d[0] for d in data])))
        record = int("".join(map(str, [d[1] for d in data])))

        min_hold, max_hold = self.find_bounds(race_time, record)
        wins = int(max_hold) - int(min_hold) + 1
        return wins


day = Day()
