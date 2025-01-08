import argparse
import logging
import sys
import time

from collections import defaultdict


def parse_input(puzzle_input: list) -> list:
    return [int(x) for x in puzzle_input[0].split(",")]

class PhysicalRobot:

    def __init__(
        self,
    ):
        self.pixels = defaultdict(int)
        self.location = (0, 0)
        self.direction = 'N'
        self.received_outputs = []
        self.visited_locations = set([(0, 0)])

    def get_pixel_value(self) -> int:
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


class ProgramState:

    def __init__(
        self,
        program: list,
        start_pointer: int = 0,
        preconfigured_inputs: list = None,
        relative_base: int = 0,
        physical_robot: PhysicalRobot = None,
    ):
        self.program = program
        self.preconfigured_inputs = preconfigured_inputs if preconfigured_inputs else []
        self.pointer = start_pointer
        self.relative_base = relative_base
        self.outputs = []
        self.halted = False
        self.physical_robot = physical_robot

    @staticmethod
    def parse_opcode(opcode: int) -> tuple:
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

    def get_parameter_values(self, opmodes: list) -> int:
        if self.pointer >= len(self.program):
            raise ValueError(
                f"Pointer {self.pointer} exceeds length of program ({len(self.program)})"
            )

        parameters = []
        for i, opmode in enumerate(opmodes):
            offset = i + 1
            if opmode == 0:  # Position mode
                index = self.program[self.pointer + offset]
                self.ensure_memory(index)
                parameter = self.program[index]

            elif opmode == 1:  # Immediate mode
                index = self.pointer + offset
                self.ensure_memory(index)
                parameter = self.program[index]

            elif opmode == 2:  # Relative mode
                index = self.program[self.pointer + offset] + self.relative_base
                self.ensure_memory(index)
                parameter = self.program[index]
            else:
                raise ValueError(f"Unrecognised opmode: {opmode}")

            parameters.append(parameter)
        return parameters

    def get_destination_index(self, offset: int, opmode: int) -> int:
        index = self.program[self.pointer + offset]
        if opmode == 2:  # Relative mode
            index += self.relative_base
        elif opmode != 0:  # Unsupported parameter mode for destination
            raise ValueError(f"Unsupported parameter mode {opmode} for destination")

        self.ensure_memory(index)  # Ensure memory is large enough for this index
        return index

    def ensure_memory(self, index: int):
        if index >= len(self.program):
            self.program.extend([0] * (index + 1 - len(self.program)))

    def execute_program(self) -> list:
        while True:
            # logging.debug(f"Pointer: {self.pointer}, Memory at pointer: {self.program[self.pointer]}")
            opcode, opmodes = self.parse_opcode(self.program[self.pointer])
            # logging.debug(f"opcode: {opcode}, opmodes: {opmodes}")

            match opcode:
                case 1:  # Add // 3 params
                    parameters = self.get_parameter_values(opmodes)
                    destination = self.get_destination_index(3, opmodes[2])
                    self.program[destination] = parameters[0] + parameters[1]
                    self.pointer += 4

                case 2:  # Multiply // 3 params
                    parameters = self.get_parameter_values(opmodes)
                    destination = self.get_destination_index(3, opmodes[2])
                    self.program[destination] = parameters[0] * parameters[1]
                    self.pointer += 4

                case 3:  # Input // 1 param
                    if self.preconfigured_inputs:
                        input_value = self.preconfigured_inputs.pop(0)
                    elif self.physical_robot:
                        input_value = self.physical_robot.get_pixel_value()
                    else:
                        input_value = int(input("Provide input value: "))

                    destination = self.get_destination_index(1, opmodes[0])
                    self.program[destination] = input_value
                    self.pointer += 2

                case 4:  # Output // 1 param
                    parameters = self.get_parameter_values(opmodes)
                    if self.physical_robot:
                        self.physical_robot.receive_output(parameters[0])

                    self.outputs.append(parameters[0])
                    self.pointer += 2

                case 5:  # Jump if true // 2 params
                    parameters = self.get_parameter_values(opmodes)
                    if parameters[0] != 0:
                        self.pointer = parameters[1]
                    else:
                        self.pointer += 3

                case 6:  # Jump if false // 2 params
                    parameters = self.get_parameter_values(opmodes)

                    if parameters[0] == 0:
                        self.pointer = parameters[1]
                    else:
                        self.pointer += 3

                case 7:  # Less than // 3 params
                    parameters = self.get_parameter_values(opmodes)
                    destination = self.get_destination_index(3, opmodes[2])
                    self.program[destination] = int(parameters[0] < parameters[1])
                    self.pointer += 4

                case 8:  # Equals // 3 params
                    parameters = self.get_parameter_values(opmodes)
                    destination = self.get_destination_index(3, opmodes[2])
                    self.program[destination] = int(parameters[0] == parameters[1])
                    self.pointer += 4

                case 9:  # Adjust relative base // 1 param
                    parameters = self.get_parameter_values(opmodes)
                    self.relative_base = self.relative_base + parameters[0]
                    self.pointer += 2

                case 99:  # Terminate with halted flag // 0 params
                    self.halted = True
                    return self.physical_robot if self.physical_robot else self


def solve_1(puzzle_input: list) -> str:
    program = parse_input(puzzle_input)
    physical_robot = PhysicalRobot()
    program_state = ProgramState(program, physical_robot=physical_robot)
    physical_robot = program_state.execute_program()

    # physical_robot.print_pixels()
    return physical_robot.count_painted_pixels()



def solve_2(puzzle_input: list) -> str:
    program = parse_input(puzzle_input)
    physical_robot = PhysicalRobot()
    program_state = ProgramState(program, preconfigured_inputs=[1], physical_robot=physical_robot)
    physical_robot = program_state.execute_program()

    physical_robot.print_pixels()
    return physical_robot.count_painted_pixels()


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
