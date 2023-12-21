# Advent of Code 2023 - Day 20

from advent_of_py import AdventDay


class Module:
    def __init__(self, name, typ):
        self.name = name
        self.outputs = []
        self.inputs = []
        self.outputting = None
        self.typ = typ
        self.pulse = None
        self.on = False
        self.mem = {}


class Day(AdventDay):
    test_files = {"2023/day20/example.txt": [11687500, None]}
    data_file = "2023/day20/data.txt"

    def parse_file(self, data):
        data = data.split("\n")[:-1]
        modules = {}
        outputs = {}
        for line in data:
            name, out = line.split(" -> ")
            out = out.split(", ")
            typ = name[0] if name[0] in {"%", "&"} else "broadcaster"
            name = name[1:] if name[0] in {"%", "&"} else name
            modules[name] = Module(name, typ)
            outputs[name] = out
        for name, outs in outputs.items():
            for o in outs:
                if o not in modules:
                    modules[o] = Module(o, "output")
                modules[name].outputs.append(modules[o])
                modules[o].inputs.append(modules[name])
        button = Module("button", "button")
        button.outputs = [modules["broadcaster"]]
        modules["broadcaster"].inputs = [button]
        modules["button"] = button
        return modules

    @classmethod
    def press_button(self, modules):
        queue = [(modules["button"], modules["broadcaster"], "low")]
        low_count, high_count, high_pulses = 0, 0, set()
        while queue:
            output_module, input_module, pulse = queue.pop(0)

            if pulse == "low":
                low_count += 1
            else:
                high_count += 1
                high_pulses.add(output_module.name)

            # flip-flop
            if input_module.typ == "%" and pulse == "low":
                input_module.on = not input_module.on
                for m in input_module.outputs:
                    queue.append(
                        (input_module, m, "high" if input_module.on else "low")
                    )
            # conjunction
            elif input_module.typ == "&":
                input_module.mem[output_module.name] = pulse
                if len(input_module.mem) == len(input_module.inputs) and set(
                    input_module.mem.values()
                ) == {"high"}:
                    out = "low"
                else:
                    out = "high"
                for m in input_module.outputs:
                    queue.append((input_module, m, out))
            elif input_module.typ not in {"%", "&"}:
                for m in input_module.outputs:
                    queue.append((input_module, m, pulse))
        return low_count, high_count, high_pulses

    def part_1_logic(self, modules):
        low_count = 0
        high_count = 0
        for i in range(1000):
            l, h, _ = self.press_button(modules)
            low_count += l
            high_count += h
        return low_count * high_count

    def part_2_logic(self, modules):
        if "rx" not in modules:
            return None
        rx_inputs = modules["rx"].inputs
        while len(rx_inputs) == 1:
            new_rx_inputs = []
            for m in rx_inputs:
                new_rx_inputs += m.inputs
            rx_inputs = new_rx_inputs

        rx_inputs = {ri.name: 0 for ri in rx_inputs}
        presses = 0
        while not all([v > 0 for v in rx_inputs.values()]):
            presses += 1
            _, _, high_pulses = self.press_button(modules)
            for rx_input in rx_inputs:
                if rx_input in high_pulses and rx_inputs[rx_input] == 0:
                    rx_inputs[rx_input] = presses

        prod = 1
        for rx_input, p in rx_inputs.items():
            prod *= p
        return prod


Day()
