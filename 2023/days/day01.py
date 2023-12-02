from advent_day import AdventDay
import re


class Day(AdventDay):
    test_files = {
        "2023/data/day01/example.txt": [142, 142],
        "2023/data/day01/example2.txt": [209, 281],
    }
    data_file = "2023/data/day01/data.txt"

    def parse_file(self, data):
        data = data.split("\n")
        return data[:-1]

    def part_1_logic(self, data):
        calibration_nums = []
        for line in data:
            calibration_num = []
            for c in line:
                if c.isnumeric():
                    calibration_num.append(c)
            if calibration_num:
                calibration_nums.append(int(calibration_num[0] + calibration_num[-1]))
        return sum(calibration_nums)

    def part_2_logic(self, data):
        s_nums = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]
        calibration_nums = []
        for line in data:
            all_nums = []
            # find all occurrences of the spelled-out numbers and their indices
            for i, s_num in enumerate(s_nums):
                occ = [m.start() for m in re.finditer(s_num, line)]
                for idx in occ:
                    all_nums.append((str(i + 1), idx))
            # find all occurrences of the digits and their indices
            for i, c in enumerate(line):
                if c.isnumeric():
                    all_nums.append((c, i))
            all_nums.sort(key=lambda x: x[1])
            calibration_nums.append(int(all_nums[0][0] + all_nums[-1][0]))
        return sum(calibration_nums)


day = Day()
