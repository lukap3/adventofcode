import re

from advent_day import AdventDay


class Day(AdventDay):
    test_files = {"2023/data/day04/example.txt": [13, 30]}
    data_file = "2023/data/day04/data.txt"

    def parse_file(self, data):
        pattern = r"Card *(\d+): *(\d+(?: *\d+)*) \| *(\d+(?: *\d+)*)"
        matches = re.findall(pattern, data)

        return [
            [
                int(card_id),
                list(map(int, first_numbers.split())),
                list(map(int, remaining_numbers.split())),
                1,
            ]
            for card_id, first_numbers, remaining_numbers in matches
        ]

    def part_1_logic(self, data):
        points = 0
        for card in data:
            card_id, card_nums, winning_nums, _ = card
            card_points = 0
            for card_num in card_nums:
                if card_num in winning_nums:
                    card_points = 1 if card_points == 0 else card_points * 2
            points += card_points
        return points

    def part_2_logic(self, data):
        for i, card in enumerate(data):
            card_id, card_nums, winning_nums, cards = card
            card_points = 0
            for card_num in card_nums:
                if card_num in winning_nums:
                    card_points += 1
            for j in range(card_points):
                data[i + j + 1][3] += cards
        num_cards = [card[3] for card in data]
        return sum(num_cards)


day = Day()
