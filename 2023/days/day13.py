from lib import AdventDay


class Day(AdventDay):
    test_files = {"2023/data/day13/example.txt": [405, 400]}
    data_file = "2023/data/day13/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        patterns = [[]]
        for line in data:
            if line == "":
                patterns.append([])
            else:
                patterns[-1].append(line)
        return patterns

    @classmethod
    def is_reflected(cls, left, right):
        if len(left) < len(right):
            right = right[: len(left)]
        if len(left) > len(right):
            left = left[-len(right) :]
        right = right[::-1]
        diffs = sum(c1 != c2 for c1, c2 in zip(left, right))
        return diffs

    @classmethod
    def find_reflection(cls, pattern, pivot=False):
        pattern = list(map(list, zip(*pattern))) if pivot else pattern
        for i in range(1, len(pattern[0])):
            split_diffs = []
            for line in pattern:
                split_diffs.append(cls.is_reflected(line[:i], line[i:]))
            if all(x == 0 for x in split_diffs):
                return i
        return 0

    @classmethod
    def find_smudged_reflection(cls, pattern, pivot=False):
        pattern = list(map(list, zip(*pattern))) if pivot else pattern
        for i in range(1, len(pattern[0])):
            split_diffs = []
            for line in pattern:
                split_diffs.append(cls.is_reflected(line[:i], line[i:]))
            if all(x == 0 or x == 1 for x in split_diffs) and split_diffs.count(1) == 1:
                return i
        return 0

    def part_1_logic(self, data):
        count = 0
        for pattern in data:
            horizontal_split = self.find_reflection(pattern)
            vertical_split = self.find_reflection(pattern, pivot=True)
            count += horizontal_split + 100 * vertical_split

        return count

    def part_2_logic(self, data):
        count = 0
        for pattern in data:
            horizontal_split = self.find_smudged_reflection(pattern)
            vertical_split = self.find_smudged_reflection(pattern, pivot=True)
            count += horizontal_split + 100 * vertical_split

        return count


day = Day()
