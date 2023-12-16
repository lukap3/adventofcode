# Advent of Code 2023 - Day 16

from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day16/example.txt": [46, 51]}
    data_file = "2023/day16/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i in range(len(data)):
            data[i] = list(data[i])
        return data

    @classmethod
    def move(cls, grid, beams, history):
        direction_map = {
            "U": lambda a, b: (a - 1, b),
            "D": lambda a, b: (a + 1, b),
            "L": lambda a, b: (a, b - 1),
            "R": lambda a, b: (a, b + 1),
        }

        mirror_map = {
            ("\\", "L"): "U",
            ("\\", "R"): "D",
            ("\\", "D"): "R",
            ("\\", "U"): "L",
            ("/", "L"): "D",
            ("/", "R"): "U",
            ("/", "D"): "L",
            ("/", "U"): "R",
        }

        new_beams = []
        for i, beam in enumerate(beams):
            pos, direction = beam
            x, y = pos
            x, y = direction_map[direction](x, y)

            # out of bounds
            if x >= len(grid) or x < 0 or y >= len(grid[x]) or y < 0:
                pass

            # continue
            elif grid[x][y] == ".":
                beams[i] = ((x, y), direction)

            # mirrors
            elif grid[x][y] in {"\\", "/"}:
                beams[i] = ((x, y), mirror_map[(grid[x][y], direction)])

            # up-down split
            elif grid[x][y] == "|":
                if direction in {"L", "R"}:
                    new_beams.append(((x, y), "U"))
                    beams[i] = ((x, y), "D")
                else:
                    beams[i] = ((x, y), direction)
            # left-right split
            elif grid[x][y] == "-":
                if direction in {"U", "D"}:
                    new_beams.append(((x, y), "L"))
                    beams[i] = ((x, y), "R")
                else:
                    beams[i] = ((x, y), direction)

        beams += new_beams
        all_beams = []
        for beam in beams:
            if beam not in history:
                all_beams.append(beam)
        return all_beams

    @classmethod
    def energize(cls, grid, start_pos, start_direction):
        beams = [(start_pos, start_direction)]
        beam_history = set()
        while beams:
            beams = cls.move(grid, beams, beam_history)
            if len(beams) == 0:
                break
            for beam in beams:
                if beam not in beam_history:
                    beam_history.add(beam)

        positions = set([position for position, _ in beam_history])
        return len(positions)

    def part_1_logic(self, data):
        return self.energize(data, (0, -1), "R")

    def part_2_logic(self, data):
        starts = []
        for x in range(len(data)):
            starts.append(((x, -1), "R"))
            starts.append(((x, len(data)), "L"))
        for y in range(len(data)):
            starts.append(((-1, y), "D"))
            starts.append(((len(data), y), "U"))
        energize_results = []
        for start in starts:
            start_pos, start_direction = start
            energize_results.append(self.energize(data, start_pos, start_direction))
        return max(energize_results)


Day()
