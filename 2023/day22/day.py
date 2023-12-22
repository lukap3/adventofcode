# Advent of Code 2023 - Day 22

from advent_of_py import AdventDay


class Brick:
    def __init__(self, idd, from_pos, to_pos):
        self.idd = idd
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.positions = self.get_positions(from_pos, to_pos)
        self.supported_by = set()

    @classmethod
    def get_positions(cls, from_pos, to_pos):
        positions = []
        for x in range(from_pos[0], to_pos[0] + 1):
            for y in range(from_pos[1], to_pos[1] + 1):
                for z in range(from_pos[2], to_pos[2] + 1):
                    positions.append((x, y, z))
        return positions

    def get_supports(self, position_map):
        p1x, p1y, p1z = self.from_pos
        p2x, p2y, p2z = self.to_pos
        new_from_pos = (p1x, p1y, p1z - 1)
        new_to_pos = (p2x, p2y, p2z - 1)
        supports = set()
        below_positions = self.get_positions(new_from_pos, new_to_pos)
        for below_position in below_positions:
            if (
                below_position in position_map
                and position_map[below_position] != self.idd
            ):
                supports.add(position_map[below_position])
        return supports

    def drop(self, position_map):
        p1x, p1y, p1z = self.from_pos
        p2x, p2y, p2z = self.to_pos
        new_from_pos = (p1x, p1y, p1z - 1)
        new_to_pos = (p2x, p2y, p2z - 1)
        if new_from_pos[2] == 0 or new_to_pos[2] == 0:
            return False

        # check if anything below
        below_positions = self.get_positions(new_from_pos, new_to_pos)
        for below_position in below_positions:
            if (
                below_position in position_map
                and position_map[below_position] != self.idd
            ):
                return False

        # update position and position_map
        self.from_pos, self.to_pos = new_from_pos, new_to_pos
        for pos in self.positions:
            del position_map[pos]
        self.positions = below_positions
        for pos in self.positions:
            position_map[pos] = self.idd

        return True


class Day(AdventDay):
    test_files = {"2023/day22/example.txt": [5, 7]}
    data_file = "2023/day22/data.txt"

    def parse_file(self, data):
        data = data.splitlines()
        bricks = []
        for i in range(len(data)):
            data[i] = data[i].split("~")
            for j in range(len(data[i])):
                data[i][j] = [int(n) for n in data[i][j].split(",")]
            bricks.append(Brick(str(i), tuple(data[i][0]), tuple(data[i][1])))

        # generate the position map
        position_map = {}
        for brick in bricks:
            for position in brick.positions:
                position_map[position] = brick.idd

        # drop all bricks to the lowest possible position
        self.drop_bricks(bricks, position_map)

        # find supporting bricks for each brick
        for brick in bricks:
            brick.supported_by = brick.get_supports(position_map)
            if len(brick.supported_by) == 0:
                brick.supported_by = {"ground"}

        # sort the bricks from lowest to highest z
        return sorted(bricks, key=lambda b: min(p[2] for p in b.positions))

    @classmethod
    def drop_bricks(cls, bricks, position_map):
        fell = True
        while fell:
            fell = False
            for brick in bricks:
                if brick.drop(position_map):
                    fell = True

    @classmethod
    def simulate_falls(cls, bricks):
        count_safe = 0
        count_cascade = 0
        for brick in bricks:
            fallen_bricks = {brick.idd}
            fall = True
            while fall:
                fall = False
                for b in bricks:
                    # if all bricks that support b fell, b falls too
                    if b.idd not in fallen_bricks and b.supported_by.issubset(
                        fallen_bricks
                    ):
                        fallen_bricks.add(b.idd)
                        fall = True
            count_safe += 1 if len(fallen_bricks) == 1 else 0
            count_cascade += len(fallen_bricks) - 1
        return count_safe, count_cascade

    def part_1_logic(self, bricks):
        count_safe, _ = self.simulate_falls(bricks)
        return count_safe

    def part_2_logic(self, bricks):
        _, count_cascade = self.simulate_falls(bricks)
        return count_cascade


Day()
