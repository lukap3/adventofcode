# Advent of Code 2023 - Day 19

import re
from collections import defaultdict
from copy import copy

from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {"2023/day19/example.txt": [19114, 167409079868000]}
    data_file = "2023/day19/data.txt"

    def parse_file(self, data):
        workflows_data, parts_data = data.split("\n\n")
        workflows = {}
        parts = []
        for line in workflows_data.split("\n"):
            workflow_id, rules = re.search(r"(.*){(.*)}", line).groups()
            rules = rules.split(",")
            workflows[workflow_id] = rules
        for line in parts_data.split("\n")[:-1]:
            part = {}
            line = line[1:-1].split(",")
            for attr in line:
                attr_name, attr_val = attr.split("=")
                part[attr_name] = int(attr_val)
            parts.append(part)
        return workflows, parts

    @classmethod
    def check_condition(cls, part, condition):
        res = re.search(r"(.*)(<|>)(\d*):(.*)", condition)
        key, op, val, dest = res.groups()
        part_value = part[key]
        if op == ">":
            if part_value > int(val):
                return dest
        elif op == "<":
            if part_value < int(val):
                return dest
        return False

    @classmethod
    def parse_condition(cls, condition):
        res = re.search(r"(.*)(<|>)(\d*):(.*)", condition)
        key, op, val, dest = res.groups()
        return key, op, val, dest

    @classmethod
    def process_part(cls, part, workflows):
        workflow_id = "in"
        while workflow_id not in {"R", "A"}:
            rules = workflows[workflow_id]
            for rule in rules:
                if ":" in rule:
                    dest = cls.check_condition(part, rule)
                    if dest:
                        workflow_id = dest
                        break
                else:
                    workflow_id = rule
                    break
        return workflow_id

    @classmethod
    def split_by_rule(cls, range_part, rule):
        viable_range_part = copy(range_part)
        nonviable_range_part = copy(range_part)

        key, op, val, dest = cls.parse_condition(rule)
        if op == "<":
            if range_part[key][1] > int(val):
                viable_range_part[key] = (viable_range_part[key][0], int(val) - 1)
                nonviable_range_part[key] = (int(val), nonviable_range_part[key][1])
        elif op == ">":
            if range_part[key][0] < int(val):
                viable_range_part[key] = (int(val) + 1, viable_range_part[key][1])
                nonviable_range_part[key] = (nonviable_range_part[key][0], int(val))

        return viable_range_part, nonviable_range_part, dest

    @classmethod
    def split_by_rules(cls, part, rules):
        dests = defaultdict(list)
        for rule in rules:
            if ":" in rule:
                s_part, f_part, dest = cls.split_by_rule(part, rule)
                if s_part is not None:
                    # the condition applies for the whole range
                    dests[dest].append(s_part)
                if f_part is not None:
                    # the condition doesn't apply for the whole range
                    part = f_part
                else:
                    return dests
            else:
                dests[rule].append(part)
        return dests

    def part_1_logic(self, data):
        workflows, parts = data
        count = 0
        for part in parts:
            dest = self.process_part(part, workflows)
            if dest == "A":
                count += sum(part.values())
        return count

    def part_2_logic(self, data):
        workflows, parts = data
        workflow_range_parts = {
            "in": [{"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}]
        }
        accepted_ranges = []
        while workflow_range_parts:
            new_range_parts = defaultdict(list)
            for workflow_id, range_parts in workflow_range_parts.items():
                if workflow_id == "A":
                    accepted_ranges += range_parts
                elif workflow_id != "R":
                    workflow = workflows[workflow_id]
                    for range_part in range_parts:
                        split_parts = self.split_by_rules(range_part, workflow)
                        for new_workflow_id, split_part_list in split_parts.items():
                            for split_part in split_part_list:
                                new_range_parts[new_workflow_id].append(split_part)

            workflow_range_parts = new_range_parts

        count = 0
        for part in accepted_ranges:
            part_rng_size = 1
            for key, (start, end) in part.items():
                part_rng_size *= end - start + 1
            count += part_rng_size
        return count


Day()
