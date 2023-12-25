# Advent of Code 2023 - Day 25

import networkx as nx
from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day25/example.txt": [54, None]}
    data_file = "2023/day25/data.txt"

    def parse_file(self, data):
        edges = []
        for i, line in enumerate(data.splitlines()):
            left, rights = line.split(": ")
            for right in rights.split(" "):
                edges.append((left, right))
        g = nx.Graph()
        g.add_edges_from(edges)
        return g

    def part_1_logic(self, graph):
        cut = nx.minimum_edge_cut(graph)
        for edge in cut:
            graph.remove_edge(*edge)
        left_node, right_node = list(cut)[0]
        left_subgraph = nx.node_connected_component(graph, left_node)
        right_subgraph = nx.node_connected_component(graph, right_node)
        return len(left_subgraph) * len(right_subgraph)

    def part_2_logic(self, data):
        return None


Day()
