from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {
        "2022/day06/example0.txt": [7, 19],
        "2022/day06/example1.txt": [5, 23],
        "2022/day06/example2.txt": [6, 23],
        "2022/day06/example3.txt": [10, 29],
        "2022/day06/example4.txt": [11, 26],
    }
    data_file = "2022/day06/data.txt"

    def parse_file(self, data):
        return data.split("\n")[0]

    @staticmethod
    def find_marker(message, marker_len=4):
        for i in range(marker_len, len(message) + 1):
            substr = message[i - marker_len : i]
            if len(set(substr)) == len(substr):
                return i
        return None

    def part_1_logic(self, data):
        return self.find_marker(data)

    def part_2_logic(self, data):
        return self.find_marker(data, marker_len=14)


day = Day()
