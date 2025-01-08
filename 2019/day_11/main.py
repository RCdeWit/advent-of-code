import argparse
import logging
import sys
import time

from collections import defaultdict


def parse_input(puzzle_input: list) -> list:
    return [int(x) for x in puzzle_input[0].split(",")]

class Executor:

    def __init__(
        self,
    ):
        self.pixels = defaultdict(int)
        self.location = (0, 0)
        self.direction = 'N'
        self.received_outputs = []
        self.visited_locations = set([(0, 0)])

    def get_input_value(self) -> int:
        return self.pixels[(self.location)]

    def receive_output(self, output_value: int) -> None:
        self.received_outputs.append(output_value)
        if len(self.received_outputs) % 2 == 1:
            self.paint_pixel(output_value)
        else:
            self.move_robot(output_value)

    def paint_pixel(self, color: int):
        # logging.debug(f'Painting {color} at {self.location}')
        self.pixels[self.location] = color

    def move_robot(self, turn: int):
        if self.direction == 'N' and turn == 0:
            self.direction = 'W'
        elif self.direction == 'N' and turn == 1:
            self.direction = 'E'

        elif self.direction == 'E' and turn == 0:
            self.direction = 'N'
        elif self.direction == 'E' and turn == 1:
            self.direction = 'S'

        elif self.direction == 'S' and turn == 0:
            self.direction = 'E'
        elif self.direction == 'S' and turn == 1:
            self.direction = 'W'

        elif self.direction == 'W' and turn == 0:
            self.direction = 'S'
        elif self.direction == 'W' and turn == 1:
            self.direction = 'N'

        x, y = self.location
        if self.direction == 'N':
            self.location = (x, y - 1)

        elif self.direction == 'E':
            self.location = (x + 1, y)

        elif self.direction == 'S':
            self.location = (x, y + 1)

        elif self.direction == 'W':
            self.location = (x - 1, y)

        self.visited_locations.add(self.location)
        # logging.debug(f"Moved {self.direction}, now at {self.location}")
        # input()

    def count_painted_pixels(self) -> int:
        return len(self.visited_locations)

    def get_visited_locations(self) -> set:
        return self.visited_locations

    def print_pixels(self) -> None:
        x_values = [key[0] for key in self.pixels]
        y_values = [key[1] for key in self.pixels]
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)

        width = max_x - min_x + 1
        height = max_y - min_y + 1
        grid = [[' ' for _ in range(width)] for _ in range(height)]

        for (x, y), value in self.pixels.items():
            if value == 1:
                grid[y - min_y][x - min_x] = '#'

        for row in grid:
            print("".join(row))


class IntCode:

    def __init__(
        self,
        program: list,
        start_pointer: int = 0,
        preconfigured_inputs: list = None,
        relative_base: int = 0,
        executor: Executor() = None,
    ):
        self.program = program.copy()
        self.preconfigured_inputs = preconfigured_inputs if preconfigured_inputs else []
        self.pointer = start_pointer
        self.relative_base = relative_base
        self.outputs = []
        self.halted = False
        self.executor = executor

    @staticmethod
    def _parse_opcode(opcode: int) -> tuple:
        result = {}
        result["opcode"] = opcode % 100
        result["opmode"] = []
        opcode = opcode // 100
        while opcode > 0:
            result["opmode"].append(opcode % 10)
            opcode = opcode // 10

        # Pad opmodes with leading zeroes
        num_parameters_per_opcode = {
            1: 3,
            2: 3,
            3: 1,
            4: 1,
            5: 2,
            6: 2,
            7: 3,
            8: 3,
            9: 1,
            99: 0,
        }

        if result["opcode"] not in num_parameters_per_opcode.keys():
            raise ValueError(
                f"Unknown opcode {opcode}: cannot pad with leading zeroes. Update `parse_opcode` method."
            )

        leading_zeroes_parameters = max(
            num_parameters_per_opcode[result["opcode"]] - len(result["opmode"]), 0
        )

        for _ in range(leading_zeroes_parameters):
            result["opmode"].append(0)

        return (result["opcode"], result["opmode"])

    def _read(self, target: int, opmode: int) -> int:
        if self.pointer >= len(self.program):
            raise ValueError(
                f"Pointer {self.pointer} exceeds length of program ({len(self.program)})"
            )

        if opmode == 0: # Position mode
            index = self.program[target]
        elif opmode == 1: # Immediate mode
            index = target
        elif opmode == 2: # Relative mode
            index = self.program[target] + self.relative_base

        self._ensure_memory(index)
        return self.program[index]

    def _get_parameter_values(self, opmodes: list) -> list:
        parameters = []
        for i, opmode in enumerate(opmodes):
            parameter_index = self.pointer + i + 1
            param = self._read(parameter_index, opmode)
            parameters.append(param)

        return parameters

    def _write(self, destination: int, value: int) -> None:
        self._ensure_memory(destination)
        self.program[destination] = value

    def _get_destination(self, offset: int, opmode: int) -> int:
        index = self.program[self.pointer + offset]
        if opmode == 2:  # Relative mode
            index += self.relative_base
        elif opmode != 0:  # Unsupported parameter mode for destination
            raise ValueError(f"Unsupported parameter mode {opmode} for destination")

        return index

    def _ensure_memory(self, index: int):
        if index >= len(self.program):
            self.program.extend([0] * (index + 1 - len(self.program)))

    def _execute_step(self, opcode: int, opmodes: list) -> None:
        match opcode:
                case 1:  # Add // 3 params
                    parameters = self._get_parameter_values(opmodes)
                    destination = self._get_destination(3, opmodes[2])
                    output = parameters[0] + parameters[1]
                    self._write(destination, output)
                    self.pointer += 4

                case 2:  # Multiply // 3 params
                    parameters = self._get_parameter_values(opmodes)
                    destination = self._get_destination(3, opmodes[2])
                    output = parameters[0] * parameters[1]
                    self._write(destination, output)
                    self.pointer += 4

                case 3:  # Input // 1 param
                    if self.preconfigured_inputs:
                        input_value = self.preconfigured_inputs.pop(0)
                    elif self.executor:
                        input_value = self.executor.get_input_value()
                    else:
                        input_value = int(input("Provide input value: "))

                    destination = self._get_destination(1, opmodes[0])
                    self._write(destination, input_value)
                    self.pointer += 2

                case 4:  # Output // 1 param
                    parameters = self._get_parameter_values(opmodes)

                    if self.executor:
                        self.executor.receive_output(parameters[0])

                    self.outputs.append(parameters[0])
                    self.pointer += 2

                case 5:  # Jump if true // 2 params
                    parameters = self._get_parameter_values(opmodes)
                    if parameters[0] != 0:
                        self.pointer = parameters[1]
                    else:
                        self.pointer += 3

                case 6:  # Jump if false // 2 params
                    parameters = self._get_parameter_values(opmodes)

                    if parameters[0] == 0:
                        self.pointer = parameters[1]
                    else:
                        self.pointer += 3

                case 7:  # Less than // 3 params
                    parameters = self._get_parameter_values(opmodes)
                    destination = self._get_destination(3, opmodes[2])
                    output = int(parameters[0] < parameters[1])
                    self._write(destination, output)
                    self.pointer += 4

                case 8:  # Equals // 3 params
                    parameters = self._get_parameter_values(opmodes)
                    destination = self._get_destination(3, opmodes[2])
                    output = int(parameters[0] == parameters[1])
                    self._write(destination, output)
                    self.pointer += 4

                case 9:  # Adjust relative base // 1 param
                    parameters = self._get_parameter_values(opmodes)
                    self.relative_base = self.relative_base + parameters[0]
                    self.pointer += 2

                case 99:  # Terminate with halted flag // 0 params
                    self.halted = True
                    return self

    def run_program(self):
        while not self.halted:
            # logging.debug(f"Pointer: {self.pointer}, Memory at pointer: {self.program[self.pointer]}")
            opcode, opmodes = self._parse_opcode(self.program[self.pointer])
            self._execute_step(opcode, opmodes)

        return self

    def show(self):
        return self


def solve_1(puzzle_input: list) -> str:
    program = parse_input(puzzle_input)
    intcode = IntCode(program, executor=Executor()).run_program()
    return intcode.show().executor.count_painted_pixels()



def solve_2(puzzle_input: list) -> str:
    program = parse_input(puzzle_input)
    intcode = IntCode(program, preconfigured_inputs=[1], executor=Executor()).run_program()
    intcode.show().executor.print_pixels()
    return intcode.show().executor.count_painted_pixels()


if __name__ == "__main__":
    # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--question", required=True)
    parser.add_argument("-i", "--input", required=False, default="input.txt")
    args = parser.parse_args()

    input_file = args.input
    question = args.question

    # Read input
    with open(input_file) as f:
        puzzle_input = list(f.read().splitlines())

    # Set up logging
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

    logging.info(f"Question {question} with input {input_file}")
    start = time.time()

    if question == "1":
        solution = solve_1(puzzle_input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    elif question == "2":
        solution = solve_2(puzzle_input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    else:
        logging.error("Select either question 1 or 2")
