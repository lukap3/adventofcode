import functools
import re
from copy import copy

from lib import AdventDay


class Day(AdventDay):
    test_files = {"2023/data/day12/example.txt": [21, 525152]}
    data_file = "2023/data/day12/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i, line in enumerate(data):
            springs, nums = line.split(" ")
            nums = [int(num) for num in nums.split(",")]
            data[i] = (springs, nums)
        return data

    @classmethod
    def fits(cls, springs, nums):
        groups = re.findall(r"(#+)", "".join(springs))
        groups = [len(group) for group in groups]
        return groups == nums

    def solve(self, springs, nums):
        if springs.count("#") > sum(nums):
            return 0
        if springs.count("?") == 0:
            if self.fits(springs, nums):
                return 1
            return 0

        permutations = 0
        for i, char in enumerate(springs):
            if char == "?":
                for option in (".", "#"):
                    new_springs = copy(springs)
                    new_springs[i] = option
                    permutations += self.solve(new_springs, nums)
                break
        return permutations

    @classmethod
    def simplify(cls, springs, nums):
        blocks = re.findall(r"[#?]+", springs)
        # remove already filled numbers and blocks from left & right
        while blocks and "#" in blocks[-1] and len(blocks[-1]) == nums[-1]:
            blocks = blocks[:-1]
            nums = nums[:-1]
        while blocks and "#" in blocks[0] and len(blocks[0]) == nums[0]:
            blocks = blocks[1:]
            nums = nums[1:]

        # remove too small blocks from left and right
        try:
            if nums[0] > len(blocks[0]):
                blocks = blocks[0:]
            if nums[-1] > len(blocks[-1]):
                blocks = blocks[:-1]
        except IndexError:
            return [], []

        # remove the [1, ...] from [?#...]
        # [2, ...] from [??#...]
        # [3, ...] from [???#...]
        first_num = nums[0]
        if blocks[0][: first_num + 1] == "?" * first_num + "#":
            blocks[0] = blocks[0][1:]

        return ".".join(blocks), nums

    @classmethod
    @functools.lru_cache()
    def permutate(cls, springs, length, nums):
        if len(nums) == 0:
            if "#" not in springs:
                return 1
            return 0

        after = sum(nums[1:]) + len(nums[1:])
        count = 0
        for before in range(length - after - nums[0] + 1):
            block = "." * before + "#" * nums[0] + "."
            if cls.can_place_block(springs, block):
                rest_springs = springs[len(block) :]
                count += cls.permutate(
                    rest_springs, length - nums[0] - before - 1, nums[1:]
                )
        return count

    @classmethod
    def can_place_block(cls, springs, block):
        for i, b in enumerate(block):
            try:
                if springs[i] != b and springs[i] != "?":
                    return False
            except IndexError:
                return True
        return True

    def part_1_logic(self, data):
        count = 0
        # bruteforce for the lulz
        for springs, nums in data:
            springs, nums = self.simplify(springs, nums)
            count += self.solve(list(springs), nums)
        return count

    def part_2_logic(self, data):
        count = 0
        for springs, nums in data:
            nums = nums * 5
            springs = "?".join([springs for _ in range(5)])
            springs, nums = self.simplify(springs, nums)
            count += self.permutate(tuple(springs), len(springs), tuple(nums))

        return count


day = Day()
