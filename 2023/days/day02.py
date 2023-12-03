import re

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"2023/data/day02/example.txt": [8, 2286]}
    data_file = "2023/data/day02/data.txt"

    def parse_file(self, data):
        data = data.split("\n")
        games = []
        for line in data[:-1]:
            game_id = int(re.findall(r"Game (\d+)", line)[0])
            rounds = []
            for r in line.split("; "):
                matches = re.findall("(\d+) (blue|red|green)", r)
                counts = {"blue": 0, "red": 0, "green": 0}
                for count, color in matches:
                    counts[color] += int(count)
                rounds.append(counts)
            games.append((game_id, rounds))
        return games

    @staticmethod
    def is_round_possible(available_cubes, r):
        for color, num in r.items():
            if num > available_cubes[color]:
                return False
        return True

    def part_1_logic(self, data):
        available_cubes = {"red": 12, "green": 13, "blue": 14}
        possible_games = []
        for game in data:
            game_id = game[0]
            rounds = game[1]
            possible_rounds = [
                self.is_round_possible(available_cubes, r) for r in rounds
            ]
            if all(possible_rounds):
                possible_games.append(game_id)

        return sum(possible_games)

    def part_2_logic(self, data):
        powers = []
        for game in data:
            max_round = {"red": 0, "green": 0, "blue": 0}
            for r in game[1]:
                for color in max_round.keys():
                    if r[color] > max_round[color]:
                        max_round[color] = r[color]
            power = 1
            for c in max_round.values():
                power *= c
            powers.append(power)
        return sum(powers)


day = Day()
