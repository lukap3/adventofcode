# Advent of Code 2023 - Day 23

import sys
from collections import defaultdict

from advent_of_py import AdventDay

sys.setrecursionlimit(10000)


class Day(AdventDay):
    test_files = {"2023/day23/example.txt": [94, 154]}
    data_file = "2023/day23/data.txt"

    def parse_file(self, data):
        return [list(line) for line in data.splitlines()]

    @classmethod
    def get_neighbours(cls, data, position, ignore_slopes=False):
        x, y = position
        slopes = {">": (x, y + 1), "<": (x, y - 1), "v": (x + 1, y), "^": (x - 1, y)}
        if data[x][y] in slopes and not ignore_slopes:
            return [slopes[data[x][y]]]
        neighbours = []
        for slope, (x_n, y_n) in slopes.items():
            if 0 <= x_n < len(data) and 0 < y_n < len(data[0]):
                if ignore_slopes and data[x_n][y_n] != "#":
                    neighbours.append((x_n, y_n))
                elif data[x_n][y_n] == "." or data[x_n][y_n] == slope:
                    neighbours.append((x_n, y_n))
        return neighbours

    @classmethod
    def find_start_end(cls, data):
        start, end = None, None
        for y in range(len(data[0])):
            if data[0][y] == ".":
                start = (0, y)
            if data[-1][y] == ".":
                end = (len(data[-1]) - 1, y)
        return start, end

    @classmethod
    def longest_path(cls, graph, position, end, path, length=0):
        if position == end:
            return length
        neighbours = graph[position]
        lengths = [0]
        for neighbour, weight in neighbours:
            if neighbour not in path:
                lengths.append(
                    cls.longest_path(
                        graph, neighbour, end, path + [position], length + weight
                    )
                )
        return max(lengths)

    @classmethod
    def build_graph(cls, data, ignore_slopes=False):
        graph = defaultdict(list)
        for x in range(len(data)):
            for y in range(len(data[x])):
                if data[x][y] != "#":
                    node = (x, y)
                    neighbours = cls.get_neighbours(data, (x, y), ignore_slopes)
                    for neighbour in neighbours:
                        graph[node].append((neighbour, 1))
        return graph

    @classmethod
    def simplify_graph(cls, graph):
        junctions = []
        for node, neighbours in graph.items():
            if len(neighbours) != 2:
                junctions.append(node)
        simple_graph = defaultdict(list)
        for junction in junctions:
            junction_neighbours = graph[junction]
            connected_junctions = []
            for junction_neighbour, _ in junction_neighbours:
                connected_junctions.append(
                    cls.find_connected_junction(graph, [junction, junction_neighbour])
                )
            simple_graph[junction] = connected_junctions
        return simple_graph

    @classmethod
    def find_connected_junction(cls, graph, path):
        node = path[-1]
        neighbours = graph[node]
        while len(neighbours) == 2:
            left_n = neighbours[0][0]
            right_n = neighbours[1][0]
            node = left_n if right_n in path else right_n
            path.append(node)
            neighbours = graph[node]
        return node, len(path) - 1

    def part_1_logic(self, data):
        start, end = self.find_start_end(data)
        graph = self.build_graph(data, ignore_slopes=False)
        return self.longest_path(graph, start, end, [])

    def part_2_logic(self, data):
        start, end = self.find_start_end(data)
        graph = self.build_graph(data, ignore_slopes=True)
        simple_graph = self.simplify_graph(graph)
        return self.longest_path(simple_graph, start, end, [])


Day()
