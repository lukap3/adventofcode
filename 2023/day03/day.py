from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day03/example.txt": [4361, 467835]}
    data_file = "2023/day03/data.txt"

    def parse_file(self, data):
        return data.split("\n")[:-1]

    @classmethod
    def extract_number(cls, line, j):
        number = ""
        while j < len(line) and line[j].isnumeric():
            number += line[j]
            j += 1
        return number, j

    @classmethod
    def extract_numbers(cls, data):
        numbers = []
        for i in range(len(data)):
            j = 0
            while j < len(data[i]):
                if data[i][j].isnumeric():
                    extracted_number, new_j = cls.extract_number(data[i], j)
                    numbers.append((extracted_number, i, j))
                    j = new_j
                j += 1
        return numbers

    @classmethod
    def get_neighbours(cls, data, i, j):
        potential_neighbours = [
            (i - 1, j),
            (i - 1, j - 1),
            (i - 1, j + 1),
            (i + 1, j),
            (i + 1, j - 1),
            (i + 1, j + 1),
            (i, j - 1),
            (i, j + 1),
        ]
        neighbours = []
        for p_n in potential_neighbours:
            n_i, n_j = p_n
            try:
                _ = data[n_i][n_j]
                neighbours.append((n_i, n_j))
            except IndexError:
                pass
        return neighbours

    @classmethod
    def check_neighbours(cls, data, i, j):
        neighbours = cls.get_neighbours(data, i, j)
        for neighbour in neighbours:
            n_i, n_j = neighbour
            point = data[n_i][n_j]
            if not point.isnumeric() and point != ".":
                return True
        return False

    def part_1_logic(self, data):
        numbers = self.extract_numbers(data)
        part_numbers = []
        for number_data in numbers:
            number, i, j = number_data
            checks = []
            for _ in range(len(number)):
                checks.append(self.check_neighbours(data, i, j))
                j += 1
            if any(checks):
                part_numbers.append(int(number))
        return sum(part_numbers)

    def part_2_logic(self, data):
        numbers = self.extract_numbers(data)

        # build a list of all numbers and their full indexes
        number_ids = []
        for number_data in numbers:
            number, i, j = number_data
            all_ids = [number]
            for offset in range(len(number)):
                all_ids.append((i, j + offset))
            number_ids.append(all_ids)

        # extract all the gear indexes
        gears = []
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == "*":
                    gears.append((i, j))

        gear_ratios = []
        for gear in gears:
            neighbour_numbers = []
            gear_neighbours = self.get_neighbours(data, gear[0], gear[1])

            # find all numbers adjacent to the gear
            for number_data in number_ids:
                if any(e in number_data for e in gear_neighbours):
                    neighbour_numbers.append(number_data[0])

            # check for errors
            if len(neighbour_numbers) > 2:
                raise Exception("FOUND TOO MANY GEAR NUMBERS")

            # calculate the gear ratio
            if len(neighbour_numbers) == 2:
                gear_ratios.append(
                    int(neighbour_numbers[0]) * int(neighbour_numbers[1])
                )

        return sum(gear_ratios)


day = Day()
