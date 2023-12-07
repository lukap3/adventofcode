from collections import Counter, defaultdict
from copy import copy
from functools import cmp_to_key

from lib import AdventDay


class Day(AdventDay):
    test_files = {"2023/data/day07/example.txt": [6440, 5905]}
    data_file = "2023/data/day07/data.txt"
    use_joker = False

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        for i in range(len(data)):
            line = data[i].split(" ")
            data[i] = (list(line[0]), int(line[1]))
        return data

    def card_value(self, card):
        card_values = {
            "T": 10,
            "J": 1 if self.use_joker else 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        if card.isdigit():
            return int(card)
        else:
            return card_values[card]

    @classmethod
    def replace_joker(cls, hand):
        # just replace the joker with the most frequent card
        if "J" in hand:
            j_hand = copy(hand)
            counter = Counter(hand)
            counter["J"] = 0
            most_common = counter.most_common()[0][0]
            for i, card in enumerate(j_hand):
                if card == "J":
                    j_hand[i] = most_common
            return j_hand
        return hand

    def score_hand(self, hand):
        counts = defaultdict(int)
        if self.use_joker:
            hand = self.replace_joker(hand)
        for card in hand:
            counts[card] += 1

        # 5 of a kind
        if 5 in counts.values():
            score = 7
        # 4 of a kind
        elif 4 in counts.values():
            score = 6
        # full house
        elif 2 in counts.values() and 3 in counts.values():
            score = 5
        # three of a kind
        elif 3 in counts.values():
            score = 4
        # two pair
        elif 2 in counts.values() and len(counts.values()) == 3:
            score = 3
        # one pair
        elif 2 in counts.values():
            score = 2
        # high card
        else:
            score = 1
        return score

    def compare_cards(self, hand1, hand2):
        for i in range(len(hand1)):
            v1 = self.card_value(hand1[i])
            v2 = self.card_value(hand2[i])
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        raise Exception("The hands are identical")

    def compare_hands(self, hand1, hand2):
        score1 = self.score_hand(hand1[0])
        score2 = self.score_hand(hand2[0])
        if score1 > score2:
            return 1
        elif score1 < score2:
            return -1
        else:
            return self.compare_cards(hand1[0], hand2[0])

    def get_winnings(self, data):
        data.sort(key=cmp_to_key(self.compare_hands))
        total_winnings = 0
        for i, hand in enumerate(data):
            rank = i + 1
            bet = hand[1]
            total_winnings += bet * rank
        return total_winnings

    def part_1_logic(self, data):
        self.use_joker = False
        return self.get_winnings(data)

    def part_2_logic(self, data):
        self.use_joker = True
        return self.get_winnings(data)


day = Day()
