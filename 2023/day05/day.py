import re

from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day05/example.txt": [35, 46]}
    data_file = "2023/day05/data.txt"

    def parse_file(self, data):
        data = data.rstrip("\n").split("\n\n")
        seeds = [int(num) for num in re.findall(r"\b\d+\b", data[0])]

        maps = {}
        for m in data[1:]:
            key = re.compile(r"(.*)-to-(.*)\smap:").search(m).groups()
            m = m.split("\n")[1:]
            maps[key] = {}
            for line in m:
                dest_start, source_start, length = [int(n) for n in line.split(" ")]
                maps[key][(source_start, source_start + length)] = (
                    dest_start,
                    dest_start + length,
                )

        return seeds, maps

    @classmethod
    def find_dest(cls, num, mp):
        for source, dest in mp.items():
            if source[0] <= num <= source[1]:
                diff = num - source[0]
                return dest[0] + diff
        return num

    @classmethod
    def merge_ranges(cls, ranges):
        sorted_ranges = sorted(ranges, key=lambda x: x[0])
        merged_ranges = []
        current_range = sorted_ranges[0]

        for start, end in sorted_ranges[1:]:
            if start <= current_range[1]:
                current_range = (current_range[0], max(current_range[1], end))
            else:
                merged_ranges.append(current_range)
                current_range = (start, end)
        merged_ranges.append(current_range)

        return merged_ranges

    @classmethod
    def find_dest_ranges(cls, ranges, mp):
        new_ranges = []
        while ranges:
            rng = ranges.pop()
            found = False
            for source, diff in mp.items():
                overlap, remainder = cls.intersect(rng, source)
                if overlap:
                    found = True
                    new_ranges.append((overlap[0] + diff, overlap[1] + diff))
                    if remainder:
                        ranges += remainder
            if not found:
                new_ranges.append(rng)
        return cls.merge_ranges(new_ranges)

    @classmethod
    def intersect(cls, range1, range2):
        min1, max1 = range1
        min2, max2 = range2
        overlap_start = max(min1, min2)
        overlap_end = min(max1, max2)
        remainder = []
        overlap = None
        if overlap_start <= overlap_end:
            overlap = (overlap_start, overlap_end)
        if min1 < min2:
            remainder.append((min1, min2 - 1))
        if max1 > max2:
            remainder.append((max2 + 1, max1))
        return overlap, remainder

    @classmethod
    def find_map(cls, have, maps):
        for key, mp in maps.items():
            if key[0] == have:
                return key[1], mp
        return None

    def part_1_logic(self, data):
        seeds, maps = data
        locations = []
        for i in range(len(seeds)):
            have = "seed"
            num = seeds[i]
            while have != "location":
                have, mp = self.find_map(have, maps)
                num = self.find_dest(num, mp)
            locations.append(num)

        return min(locations)

    def part_2_logic(self, data):
        seeds, maps = data
        ranges = [
            (seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)
        ]

        for key in maps:
            for rng in maps[key]:
                new_rng = maps[key][rng]
                diff = new_rng[0] - rng[0]
                maps[key][rng] = diff

        have = "seed"
        while have != "location":
            have, mp = self.find_map(have, maps)
            ranges = self.find_dest_ranges(ranges, mp)

        lows = [rng[0] for rng in ranges]
        return min(lows)


day = Day()
