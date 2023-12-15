from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day14/example.txt": [136, 64]}
    data_file = "2023/day14/data.txt"

    direction_sorts = {
        "N": lambda x: sorted(x, key=lambda e: e[0]),
        "W": lambda x: sorted(x, key=lambda e: e[1]),
        "S": lambda x: sorted(x, key=lambda e: e[0], reverse=True),
        "E": lambda x: sorted(x, key=lambda e: e[1], reverse=True),
    }

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i in range(len(data)):
            data[i] = list(data[i])
        return data

    @classmethod
    def tilt(cls, data, direction):
        size = len(data)

        # last_cube, range, pivot, placement
        direction_setups = {
            "N": (-1, range(size), False, 1),
            "S": (size, range(size - 1, -1, -1), False, -1),
            "W": (-1, range(size), True, 1),
            "E": (size, range(size - 1, -1, -1), True, -1),
        }

        default_last_cube, rng, pivot, placement = direction_setups[direction]

        for row_col in range(size):
            last_cube = default_last_cube
            for x in rng:
                e = data[row_col][x] if pivot else data[x][row_col]
                if e == "#":
                    last_cube = x
                if e == "O":
                    last_cube += placement
                    if pivot:
                        data[row_col][x] = "."
                        data[row_col][last_cube] = "O"
                    else:
                        data[x][row_col] = "."
                        data[last_cube][row_col] = "O"

        return data

    @classmethod
    def cycle(cls, data):
        for direction in ["N", "W", "S", "E"]:
            data = cls.tilt(data, direction)
        return data

    @classmethod
    def to_hashable(cls, data):
        return tuple(tuple(row) for row in data)

    def part_1_logic(self, data):
        data = self.tilt(data, "N")

        count = 0
        for i, row in enumerate(data):
            count += (len(data) - i) * row.count("O")

        return count

    def part_2_logic(self, data):
        cycles = 1000000000

        setups = {}
        cycles_left = 0
        for i in range(cycles):
            data = self.cycle(data)
            hashable = self.to_hashable(data)
            if hashable in setups:
                cycles_left = (cycles - i) % (i - setups[hashable]) - 1
                break
            setups[hashable] = i

        for i in range(cycles_left):
            data = self.cycle(data)

        count = 0
        for i, row in enumerate(data):
            count += (len(data) - i) * row.count("O")
        return count


day = Day()
