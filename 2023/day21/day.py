# Advent of Code 2023 - Day 21

import numpy as np
from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day21/example.txt": [42, 528192461129799]}
    data_file = "2023/day21/data.txt"

    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i in range(len(data)):
            data[i] = list(data[i])
        return data

    @classmethod
    def get_neighbours(cls, grid, position, inf=False):
        x, y = position
        neighbours = []
        for mx, my in cls.moves:
            nx = x + mx
            ny = y + my
            if not inf:
                if (
                    0 <= nx < len(grid)
                    and 0 <= ny < len(grid[0])
                    and grid[nx][ny] != "#"
                ):
                    neighbours.append((nx, ny))
            else:
                mod_x = nx % len(grid)
                mod_y = ny % len(grid[0])
                if grid[mod_x][mod_y] != "#":
                    neighbours.append((nx, ny))
        return neighbours

    @classmethod
    def next_steps(cls, grid, positions, inf=False):
        new_positions = []
        for position in positions:
            if not inf:
                new_positions += cls.get_neighbours(grid, position)
            else:
                new_positions += cls.get_neighbours(grid, position, True)

        return set(new_positions)

    @classmethod
    def get_diffs(cls, numbers):
        diffs = []
        for i in range(1, len(numbers)):
            diffs.append(numbers[i] - numbers[i - 1])
        return diffs

    @classmethod
    def find_start(cls, grid):
        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] == "S":
                    return x, y
        return None

    def part_1_logic(self, grid):
        start = self.find_start(grid)
        positions = [start]
        for i in range(64):
            positions = self.next_steps(grid, positions)
        return len(positions)

    def part_2_logic(self, grid):
        start = self.find_start(grid)
        positions = [start]
        nums = [1]
        target_steps = 26501365
        full_grid = len(grid)
        half_grid = int(full_grid / 2)

        # generate enough numbers to use in extrapolation
        for i in range(full_grid * 3):
            positions = self.next_steps(grid, positions, inf=True)
            nums.append(len(positions))

        nums = nums[half_grid:]
        # check for patterns
        step_size = 0
        while True:
            step_size += 1
            s_nums = []
            for i in range(0, len(nums), step_size):
                s_nums.append(nums[i])
            last_3 = s_nums[-3:]
            num_diffs = self.get_diffs(last_3)
            diff_diffs = self.get_diffs(num_diffs)
            if len(set(diff_diffs)) == 1 and full_grid % step_size == 0:
                break

        first_3 = [nums[i] for i in range(0, full_grid * 3, full_grid)]
        target = (target_steps - half_grid) // full_grid

        # y = ax2 + bx + c
        coefficients = np.polyfit([0, 1, 2], first_3, 2)
        result = np.polyval(coefficients, target)

        return round(float(result))


Day()
