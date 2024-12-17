import argparse
import logging
import sys
import time


def parse_input(input: list) -> (list, list):
    register_a = int(input[0].split(": ")[1])
    register_b = int(input[1].split(": ")[1])
    register_c = int(input[2].split(": ")[1])
    program = list(map(int, input[4].split(": ")[1].split(",")))

    return register_a, register_b, register_c, program

def parse_instruction(program: list) -> list:
    output = []
    for i in range(0, len(program), 2):
        opcode = program[i]
        operand = program[i+1]
        instruction = get_instruction(opcode)
        # logging.debug(f"Instruction {i//2}: {instruction} {operand}")
        output.append((instruction, operand))
    return output

def get_instruction(opcode: int) -> str:
    instructions = {
        0: "adv", # division
        1: "bxl", # bitwise XOR 
        2: "bst", # combo operand modulo 8
        3: "jnz", # does nothing if A==0, else jump
        4: "bxc", # bitwise XOR of B and C then store in B
        5: "out", # combo operand mod 8 then output
        6: "bdv", # same as adv but store in B
        7: "cdv", # same as adv but store in C
    }

    return instructions[opcode]

def get_combo_operand(operand: int, registers: list) -> int:
    reg_a, reg_b, reg_c = registers

    if operand == 0:
        return 0
    elif operand == 1:
        return 1
    elif operand == 2:
        return 2
    elif operand == 3:
        return 3
    elif operand == 4:
        return reg_a
    elif operand == 5:
        return reg_b
    elif operand == 6:
        return reg_c
    elif operand == 7:
        return None

def execute_instruction(instruction: tuple, registers: list, current_instruction_index: int) -> (list, int, int):
    ### Returns new registers, the next instruction index, and possibly an output
    reg_a, reg_b, reg_c = registers
    opcode, operand = instruction

    if opcode == "adv":
        numerator = reg_a
        denominator = 2 ** get_combo_operand(operand, registers)
        result = numerator // denominator
        return [result, reg_b, reg_c], current_instruction_index + 1, None
    elif opcode == "bxl":
        result = reg_b ^ operand
        return [reg_a, result, reg_c], current_instruction_index + 1, None
    elif opcode == "bst":
        result = get_combo_operand(operand, registers) % 8
        return [reg_a, result, reg_c], current_instruction_index + 1, None
    elif opcode == "jnz":
        if reg_a == 0:
            return [reg_a, reg_b, reg_c], current_instruction_index + 1, None
        else:
            return [reg_a, reg_b, reg_c], operand, None
    elif opcode == "bxc":
        result = reg_b ^ reg_c
        return [reg_a, result, reg_c], current_instruction_index + 1, None
    elif opcode == "out":
        result = get_combo_operand(operand, registers) % 8
        # logging.info(f"OUTPUT: {result}")
        return [reg_a, reg_b, reg_c], current_instruction_index + 1, result
    elif opcode == "bdv":
        numerator = reg_a
        denominator = 2 ** get_combo_operand(operand, registers)
        result = numerator // denominator
        return [reg_a, result, reg_c], current_instruction_index + 1, None
    elif opcode == "cdv":
        numerator = reg_a
        denominator = 2 ** get_combo_operand(operand, registers)
        result = numerator // denominator
        return [reg_a, reg_b, result], current_instruction_index + 1, None

    raise ValueError(f"Unknown opcode: {opcode}")
    


def solve_1(input: list) -> str:
    register_a, register_b, register_c, program = parse_input(input)
    # logging.debug(f"Registers: {register_a}, {register_b}, {register_c}")
    # logging.debug(f"Program: {program}")
    instructions = parse_instruction(program)
    logging.debug(f"Instructions: {instructions}")

    outputs = []
    current_instruction_index = 0
    while current_instruction_index < len(instructions):
        registers = [register_a, register_b, register_c]
        instruction = instructions[current_instruction_index]
        registers, current_instruction_index, output = execute_instruction(instruction, registers, current_instruction_index)
        register_a, register_b, register_c = registers
        if output is not None:
            outputs.append(str(output))

    return ",".join(outputs)

def solve_2(input: list) -> int:
    pass


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
