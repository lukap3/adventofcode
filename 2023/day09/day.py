from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day09/example.txt": [114, 2]}
    data_file = "2023/day09/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i in range(len(data)):
            data[i] = [int(n) for n in data[i].split(" ")]
        return data

    def extrapolate(self, nums):
        diffs = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
        if len(set(diffs)) == 1:
            return nums[-1] + diffs[0]
        else:
            return nums[-1] + self.extrapolate(diffs)

    def part_1_logic(self, data):
        extrapolated = []
        for nums in data:
            extrapolated.append(self.extrapolate(nums))
        return sum(extrapolated)

    def part_2_logic(self, data):
        extrapolated = []
        for nums in data:
            extrapolated.append(self.extrapolate(nums[::-1]))
        return sum(extrapolated)


day = Day()
