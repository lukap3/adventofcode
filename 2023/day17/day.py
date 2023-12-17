# Advent of Code 2023 - Day 17

from advent_of_py import AdventDay


class Day(AdventDay):
    test_files = {
        "2023/day17/example.txt": [102, 94],
        "2023/day17/example2.txt": [59, 71],
    }
    data_file = "2023/day17/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        return [[int(n) for n in list(line)] for line in data]

    @classmethod
    def get_moves(cls, grid, position, path, ultra=False):
        moves = {
            "L": lambda p, n: (p[0], p[1] - n),
            "R": lambda p, n: (p[0], p[1] + n),
            "U": lambda p, n: (p[0] - n, p[1]),
            "D": lambda p, n: (p[0] + n, p[1]),
        }
        reverse = {"L": "R", "R": "L", "U": "D", "D": "U", "X": "X"}
        last_direction = path[-1][0] if len(path) > 0 else "X"
        viable_moves = []

        rng = range(1, 10) if ultra else range(1, 4)
        min_step = 4 if ultra else 1

        for direction, gen in moves.items():
            if direction != last_direction and direction != reverse[last_direction]:
                cost = 0
                for i in rng:
                    new_position = gen(position, i)
                    new_x, new_y = new_position
                    if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                        cost += grid[new_x][new_y]
                        if i >= min_step:
                            viable_moves.append((direction, i, new_position, cost))
                    else:
                        break
        return viable_moves

    def get_path(self, grid, ultra=False):
        # worst case scenario -only 9s everywhere
        min_cost = (len(grid) - 1) * 9 + (len(grid[0]) - 1) * 9
        target = (len(grid) - 1, len(grid[0]) - 1)

        # direction, position: path to position, cost to position
        queue = {("X", (0, 0)): ([], 0)}

        # direction, position: minimum seen cost to position
        visited = {}

        min_path = None
        while len(queue):
            for position_key in list(queue.keys()):
                direction, position = position_key

                # check if target is hit, update min_path and min_cost
                if position == target and queue[position_key][1] < min_cost:
                    min_path, min_cost = queue[position_key]

                path, cost = queue.pop(position_key)
                moves = self.get_moves(grid, position, path, ultra)

                for move in moves:
                    new_direction, steps, new_position, move_cost = move
                    new_position_key = (new_direction, new_position)
                    new_cost = cost + move_cost
                    # skip if already visited from the same direction and lower cost
                    if (new_direction, new_position) in visited and visited[
                        (new_direction, new_position)
                    ] <= new_cost:
                        continue
                    # skip if this path is more expensive than the cheapest found path to target
                    elif new_cost >= min_cost:
                        continue
                    # update the queue and visited if not visited yet or cheaper
                    elif (
                        new_position_key not in visited
                        or new_cost < visited[new_position_key]
                    ):
                        queue[new_position_key] = (path + [new_position_key], new_cost)
                        visited[(new_direction, new_position)] = new_cost

        return min_cost, min_path

    def part_1_logic(self, data):
        min_cost, min_path = self.get_path(data)
        return min_cost

    def part_2_logic(self, data):
        min_cost, min_path = self.get_path(data, ultra=True)
        return min_cost


Day()
