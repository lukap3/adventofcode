from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day15/example.txt": [1320, 145]}
    data_file = "2023/day15/data.txt"

    def parse_file(self, data):
        return data.split("\n")[0].split(",")

    @classmethod
    def hash(cls, word):
        val = 0
        for char in word:
            val += ord(char)
            val *= 17
            val = val % 256
        return val

    @classmethod
    def replace_lens(cls, boxes, label, focal_length):
        hash_val = cls.hash(label)
        for i, lens in enumerate(boxes[hash_val]):
            lens_label, lens_focal_length = lens
            if lens_label == label:
                boxes[hash_val][i] = (label, focal_length)
                return
        boxes[hash_val].append((label, focal_length))

    @classmethod
    def remove_lens(cls, boxes, label):
        hash_val = cls.hash(label)
        for i, lens in enumerate(boxes[hash_val]):
            lens_label, _ = lens
            if lens_label == label:
                del boxes[hash_val][i]
                return

    @classmethod
    def get_focus_power(cls, boxes):
        focus_power = 0
        for i, box in enumerate(boxes):
            for j, lens in enumerate(box):
                focus_power += (1 + i) * (1 + j) * lens[1]
        return focus_power

    def part_1_logic(self, data):
        hash_val = 0
        for word in data:
            hash_val += self.hash(word)
        return hash_val

    def part_2_logic(self, data):
        boxes = [[] for _ in range(256)]
        for word in data:
            if "=" in word:
                label, focus_length = word.split("=")
                self.replace_lens(boxes, label, int(focus_length))
            elif word[-1] == "-":
                label = word[:-1]
                self.remove_lens(boxes, label)
        return self.get_focus_power(boxes)


day = Day()
