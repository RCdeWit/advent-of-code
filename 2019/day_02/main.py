import argparse
import logging
import sys
import time

def parse_input(input: list) -> list:
    return [int(x) for x in input[0].split(',')]

def execute_program(program: list) -> list:
    pointer = 0

    while True:
        opcode = program[pointer]

        match opcode:
            case 1:
                # Add
                program[program[pointer + 3]] = program[program[pointer + 1]] + program[program[pointer + 2]]
                num_parameters = 3
            case 2:
                # Multiply
                program[program[pointer + 3]] = program[program[pointer + 1]] * program[program[pointer + 2]]
                num_parameters = 3
            case 99:
                # Terminate
                return program
            
        pointer += num_parameters + 1

        if pointer >= len(program):
            return program


def solve_1(input: list) -> str:
    program = parse_input(input)

    program[1] = 12
    program[2] = 2

    program = execute_program(program)
    return program[0]

def solve_2(input: list) -> str:
    program = parse_input(input)

    for noun in range(100):
        for verb in range(100):
            program_copy = program.copy()
            program_copy[1] = noun
            program_copy[2] = verb

            program_copy = execute_program(program_copy)

            if program_copy[0] == 19690720:
                return 100 * noun + verb

    program = execute_program(program)
    return program[0]

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
        input = list(f.read().splitlines())

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
        solution = solve_1(input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    elif question == "2":
        solution = solve_2(input)
        logging.info(f"Found solution: {solution} (in {time.time()-start} seconds)")
    else:
        logging.error("Select either question 1 or 2")
