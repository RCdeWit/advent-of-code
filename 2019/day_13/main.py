import argparse
import logging
import sys
import time

import readchar


def parse_input(puzzle_input: list) -> list:
    return [int(x) for x in puzzle_input[0].split(",")]

class Executor:

    def __init__(
        self,
        program,
        coins = 0,
        cheat = False
    ):
        program[0] = coins
        self.screen = []
        self.joystick = (0, 0)
        self.ball = (0, 0)
        self.score = 0
        self.blocks_remaining = 0
        self.intcode = IntCode(program, input_callback=self.provide_input, output_callback=self.process_output)
        self.cheat = cheat
        self._temp_output = []

    def run(self):
        self.intcode.run_program()

    def count_tiles(self, tile: int):
        result = 0
        for i, output in enumerate(self.intcode.show().outputs):
            if i % 3 == 2 and output == tile:
                result += 1

        return result

    def provide_input(self) -> int:
        sys.stdout.flush()
        self.draw_screen()

        if self.cheat:
            if self.ball[0] < self.joystick[0]:
                self.joystick = (self.joystick[0] - 1, self.joystick[1])
                return -1 
            elif self.ball[0] > self.joystick[0]:
                self.joystick = (self.joystick[0] + 1, self.joystick[1])
                return 1
            else:
                return 0
        
        print('Use joystick (ASD)')
        control = readchar.readchar()

        if control in ("a", "A"):
            self.joystick = (self.joystick[0] - 1, self.joystick[1])
            return -1 
        elif control in ("d", "D"):
            self.joystick = (self.joystick[0] + 1, self.joystick[1])
            return 1
        elif control in ("s", "S"):
            return 0

    def process_output(self, value):
        """Process outputs in groups of 3 (x, y, tile) to track game state"""
        self._temp_output.append(value)
        
        if len(self._temp_output) == 3:
            x, y, tile = self._temp_output
            
            # Track score updates
            if x == -1 and y == 0:
                self.score = tile
            # Track block count
            elif tile == 2:
                self.blocks_remaining += 1
            elif self._last_tile_at(x, y) == 2 and tile == 0:
                self.blocks_remaining -= 1
                if self.blocks_remaining == 0:
                    # Force a score update when last block is broken
                    self.score = self.score  # This will trigger the display
            
            # Store the result before clearing
            result = tile
            
            # Clear the buffer
            self._temp_output = []
            
            return result
        
        return value

    def _last_tile_at(self, x, y):
        for i in range(len(self.intcode.outputs) - 3, -1, -3):
            if self.intcode.outputs[i-2] == x and self.intcode.outputs[i-1] == y:
                return self.intcode.outputs[i]
        return 0


    def draw_screen(self):
        tiles = {}
        max_x = 0
        max_y = 0
        for i, output in enumerate(self.intcode.show().outputs):
            if i % 3 == 0:
                x = output
                max_x = max(x, max_x)
            elif i % 3 == 1:
                y = output
                max_y = max(y, max_y)
            elif i % 3 == 2:
                if x == -1 and y == 0:
                    self.score = output
                    continue
                else:
                    match output:
                        case 0:
                            tile = " "
                        case 1:
                            tile = "+"
                        case 2:
                            tile = "#"
                        case 3:
                            tile = "_"
                            self.joystick = (x, y)
                        case 4:
                            tile = "o"
                            self.ball = (x, y)

                    tiles[(x, y)] = tile

        screen = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for coordinate, tile in tiles.items():
            x, y = coordinate
            screen[y][x] = tile

        for row in screen:
            print("".join(row))

        print(self.score)


class IntCode:

    def __init__(
        self,
        program: list,
        start_pointer: int = 0,
        preconfigured_inputs: list = None,
        relative_base: int = 0,
        input_callback = None,
        output_callback = None
    ):
        self.program = program.copy()
        self.preconfigured_inputs = preconfigured_inputs if preconfigured_inputs else []
        self.pointer = start_pointer
        self.relative_base = relative_base
        self.outputs = []
        self.halted = False
        self.input_callback = input_callback
        self.output_callback = output_callback

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
                    elif self.input_callback:
                        input_value = self.input_callback()
                    else:
                        input_value = int(input("Provide input value: "))

                    destination = self._get_destination(1, opmodes[0])
                    self._write(destination, input_value)
                    self.pointer += 2

                case 4:  # Output // 1 param
                    parameters = self._get_parameter_values(opmodes)
                    output_value = parameters[0]

                    if self.output_callback:
                        output_value = self.output_callback(output_value)

                    self.outputs.append(output_value)
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
    arcade = Executor(program)
    arcade.run()

    arcade.draw_screen()

    return arcade.count_tiles(2)

def solve_2(puzzle_input: list) -> str:
    program = parse_input(puzzle_input)
    arcade = Executor(program, coins=2, cheat=True)
    arcade.run()

    return arcade.score


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
