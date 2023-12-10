from lib import AdventDay


class Day(AdventDay):
    test_files = {
        "2023/data/day10/example.txt": [4, 1],
        "2023/data/day10/example2.txt": [8, 1],
        "2023/data/day10/example3.txt": [23, 4],
        "2023/data/day10/example4.txt": [70, 8],
    }
    data_file = "2023/data/day10/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        return [list(line) for line in data]

    @classmethod
    def find_start(cls, data):
        for x, line in enumerate(data):
            for y, c in enumerate(line):
                if c == "S":
                    return x, y
        raise Exception("S missing in data")

    @classmethod
    def get_neighbours(cls, data, position):
        x, y = position
        viable_map = {
            "F": [(x, y + 1), (x + 1, y)],
            "J": [(x, y - 1), (x - 1, y)],
            "|": [(x + 1, y), (x - 1, y)],
            "-": [(x, y + 1), (x, y - 1)],
            "L": [(x - 1, y), (x, y + 1)],
            "7": [(x + 1, y), (x, y - 1)],
            ".": [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)],
            "█": [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)],
        }
        if data[x][y] != "S":
            return viable_map[data[x][y]]
        s_neighbours = []
        for viable_n in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            reverse_neighbours = cls.get_neighbours(data, viable_n)
            for reverse_n in reverse_neighbours:
                if data[reverse_n[0]][reverse_n[1]] == "S":
                    s_neighbours.append(viable_n)
        return s_neighbours

    @classmethod
    def find_loop(cls, data):
        start = cls.find_start(data)
        visited = [start]
        found_next = True
        while found_next:
            neighbours = cls.get_neighbours(data, visited[-1])
            found_next = False
            for neighbour in neighbours:
                if neighbour not in visited:
                    found_next = True
                    visited.append(neighbour)
                    break
        return visited

    @classmethod
    def inflate(cls, char):
        empty = [".", ".", "."]
        vertical = [".", "|", "."]
        horizontal = ["-", "-", "-"]
        inflate_rules = {
            "F": [empty, [".", "F", "-"], vertical],
            "J": [vertical, ["-", "J", "."], empty],
            "|": [vertical, vertical, vertical],
            "-": [empty, horizontal, empty],
            "L": [vertical, [".", "L", "-"], empty],
            "7": [empty, ["-", "7", "."], vertical],
            ".": [empty, empty, empty],
            "S": [[".", "S", "."], ["S", "S", "S"], [".", "S", "."]],
        }
        return inflate_rules[char]

    @classmethod
    def inflate_map(cls, data):
        for i, row in enumerate(data):
            for j, char in enumerate(row):
                data[i][j] = cls.inflate(char)

        inflated = []
        for i, row in enumerate(data):
            for c in range(3):
                s_row = []
                for j, block in enumerate(row):
                    s_row += block[c]
                inflated.append(s_row)

        return inflated

    @classmethod
    def deflate_map(cls, data):
        deflated = []
        for x in range(1, len(data), 3):
            row = []
            for y in range(1, len(data[x]), 3):
                row.append(data[x][y])
            deflated.append(row)
        return deflated

    @classmethod
    def flood(cls, data, position):
        x, y = position
        if data[x][y] != ".":
            return data

        to_flood = [position]
        while len(to_flood) > 0:
            x_f, y_f = to_flood.pop()
            data[x_f][y_f] = "█"
            for n_pos in cls.get_neighbours(data, (x_f, y_f)):
                x_n, y_n = n_pos
                try:
                    if data[x_n][y_n] == ".":
                        to_flood.append(n_pos)
                except IndexError:
                    pass
        return data

    def part_1_logic(self, data):
        visited = self.find_loop(data)
        return int(len(visited) / 2)

    def part_2_logic(self, data):
        visited = self.find_loop(data)

        # remove all pipes not in the main loop
        for x in range(len(data)):
            for y in range(len(data[x])):
                if (x, y) not in visited:
                    data[x][y] = "."

        # inflate the map
        data = self.inflate_map(data)

        # flood the edges
        top_edge = [(0, j) for j in range(len(data[0]))]
        bottom_edge = [(len(data) - 1, j) for j in range(len(data[0]))]
        left_edge = [(i, 0) for i in range(1, len(data) - 1)]
        right_edge = [(i, len(data[i]) - 1) for i in range(1, len(data) - 1)]
        edge_positions = set(top_edge + bottom_edge + left_edge + right_edge)
        for edge_position in edge_positions:
            data = self.flood(data, edge_position)

        # deflate the map
        data = self.deflate_map(data)

        # count non-flooded spaces
        count = 0
        for row in data:
            for char in row:
                if char == ".":
                    count += 1
        return count


day = Day()
