import argparse
import logging
import sys
import time

from itertools import permutations

def parse_input(puzzle_input: list) -> list:
    return [int(x) for x in puzzle_input[0].split(",")]

def parse_opcode(opcode: int) -> tuple:
    result = {}
    result['opcode'] = opcode % 100
    result['opmode'] = []
    opcode = opcode // 100
    while opcode > 0:
        result['opmode'].append(opcode % 10)
        opcode = opcode // 10

    # Pad opmodes with leading zeroes
    if result['opcode'] in (3, 4, 99):
        leading_zeroes_parameters = 0
    elif result['opcode'] in (1, 2):
        leading_zeroes_parameters = 3 - len(result['opmode'])
    elif result['opcode'] in (5, 6, 7, 8):
        leading_zeroes_parameters = 2 - len(result['opmode'])
    else:
        raise ValueError(f"Unknown opcode {opcode}: cannot pad with leading zeroes. Update `parse_opcode` method.")

    for _ in range(leading_zeroes_parameters):
        result['opmode'].append(0)

    return (result['opcode'], result['opmode'])

def get_parameter_value(program: list, pointer: int, opmode: int) -> int:
    if opmode == 0:
        return program[program[pointer]]
    elif opmode == 1:
        return program[pointer]
    elif pointer > len(program):
        raise ValueError(f'Pointer {pointer} exceeds length of program ({len(program)})')
        exit()
    else:
        raise ValueError(f'Unrecognised opmode: {opmode}')
        exit()

def execute_program(program: list, preconfigured_inputs: list = None, start_pointer: int = 0) -> list:
    outputs = []
    pointer = start_pointer
    while True:
        # logging.debug(f"Current pointer: {pointer}, opcode {program[pointer]}")
        opcode, opmodes = parse_opcode(program[pointer])
        # logging.debug(f"opcode: {opcode}, opmodes: {opmodes}")

        match opcode:
            case 1: # Add
                parameter_1 = get_parameter_value(program, pointer + 1, opmodes[0])
                parameter_2 = get_parameter_value(program, pointer + 2, opmodes[1])
                destination = program[pointer + 3]
                program[destination] = parameter_1 + parameter_2
                pointer += 4

            case 2: # Multiply
                parameter_1 = get_parameter_value(program, pointer + 1, opmodes[0])
                parameter_2 = get_parameter_value(program, pointer + 2, opmodes[1])
                destination = program[pointer + 3]
                program[destination] = parameter_1 * parameter_2
                pointer += 4

            case 3: # Input
                if preconfigured_inputs is None:
                    input_value = int(input('Provide input value: '))
                if not preconfigured_inputs:
                    # Return current state while waiting for input
                    return program, outputs, pointer, False
                else:
                    input_value = preconfigured_inputs.pop(0)

                program[program[pointer + 1]] = input_value
                pointer += 2
                
            case 4: # Output
                # logging.info(f"OUTPUT: {program[program[pointer + 1]]}")
                outputs.append(program[program[pointer + 1]])
                pointer += 2

            case 5: # Jump if true
                parameter_1 = get_parameter_value(program, pointer + 1, opmodes[0])
                parameter_2 = get_parameter_value(program, pointer + 2, opmodes[1])

                if parameter_1 != 0:
                    pointer = parameter_2
                else:
                    pointer += 3

            case 6: # Jump if false
                parameter_1 = get_parameter_value(program, pointer + 1, opmodes[0])
                parameter_2 = get_parameter_value(program, pointer + 2, opmodes[1])

                if parameter_1 == 0:
                    pointer = parameter_2
                else:
                    pointer += 3

            case 7: # Less than
                parameter_1 = get_parameter_value(program, pointer + 1, opmodes[0])
                parameter_2 = get_parameter_value(program, pointer + 2, opmodes[1])
                destination = program[pointer + 3]

                program[destination] = int(parameter_1 < parameter_2)
                pointer += 4

            case 8: # Equals
                parameter_1 = get_parameter_value(program, pointer + 1, opmodes[0])
                parameter_2 = get_parameter_value(program, pointer + 2, opmodes[1])
                destination = program[pointer + 3]
                
                program[destination] = int(parameter_1 == parameter_2)
                pointer += 4

            case 99:
                # Terminate with halted flag
                return program, outputs, pointer, True

        if pointer >= len(program):
            return program, outputs, pointer, True 


def solve_1(puzzle_input: list) -> str:
    program = parse_input(puzzle_input)

    # logging.debug(f"INPUT: {program}")
    possible_sequences = list(permutations([0, 1, 2, 3, 4]))

    high_score = 0
    for sequence in possible_sequences:
        previous = 0
        for phase in sequence:
            temp_program = program.copy()
            _, outputs = execute_program(temp_program, preconfigured_inputs=[phase, previous])
            previous = outputs[0]

        high_score = max(high_score, previous)
    # logging.debug(f"RESULT: {program}")
    return high_score

def solve_2(puzzle_input: list) -> str:
    program = parse_input(puzzle_input)

    # logging.debug(f"INPUT: {program}")
    possible_sequences = list(permutations([5, 6, 7, 8, 9]))

    high_score = 0
    for sequence in possible_sequences:
        amps = [{'program': program.copy(), 'pointer': 0, 'inputs': [phase]} for phase in sequence]
        amps[0]['inputs'].append(0)

        halted = [False] * 5
        last_output = 0
        
        while not all(halted):
            for i in range(5):
                if halted[i]:
                    continue
                    
                amp = amps[i]
                prog, out, pointer, is_halted = execute_program(
                    amp['program'], 
                    amp['inputs'], 
                    amp['pointer']
                )
                
                amp['program'] = prog
                amp['pointer'] = pointer
                halted[i] = is_halted
                
                if out:
                    next_amp = (i + 1) % 5
                    amps[next_amp]['inputs'].extend(out)
                    if next_amp == 0:
                        last_output = out[-1]
        
        high_score = max(high_score, last_output)

    return high_score


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
