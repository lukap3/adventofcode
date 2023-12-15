from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day11/example.txt": [374, 82000210]}
    data_file = "2023/day11/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i in range(len(data)):
            data[i] = list(data[i])
        return data

    @classmethod
    def distance_m(cls, star1, star2, expansion, factor=1):
        x1, y1 = star1
        x2, y2 = star2
        distance = abs(x1 - x2) + abs(y1 - y2)

        x_expansion, y_expansion = expansion
        for i in range(min(y1, y2) + 1, max(y1, y2)):
            if i in y_expansion:
                distance += factor - 1

        for j in range(min(x1, x2) + 1, max(x1, x2)):
            if j in x_expansion:
                distance += factor - 1

        return distance

    @classmethod
    def get_expansion(cls, data):
        x_expansion = []
        y_expansion = []

        # find rows that expanded
        for i in range(len(data)):
            if "#" not in data[i]:
                x_expansion.append(i)
        data = list(map(list, zip(*data)))

        # find columns that expanded
        for i in range(len(data)):
            if "#" not in data[i]:
                y_expansion.append(i)

        return x_expansion, y_expansion

    @classmethod
    def get_stars(cls, data):
        stars = []
        for x in range(len(data)):
            for y in range(len(data[x])):
                if data[x][y] == "#":
                    stars.append((x, y))
        return stars

    @classmethod
    def get_sum_distances(cls, data, factor):
        expansion = cls.get_expansion(data)
        stars = cls.get_stars(data)

        distances = 0
        for i in range(len(stars)):
            for j in range(i, len(stars)):
                distances += cls.distance_m(stars[i], stars[j], expansion, factor)
        return distances

    def part_1_logic(self, data):
        return self.get_sum_distances(data, factor=2)

    def part_2_logic(self, data):
        return self.get_sum_distances(data, factor=1000000)


day = Day()
