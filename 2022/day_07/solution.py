import argparse
import sys

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-q", "--question", required=True)
args = parser.parse_args()

input_file = args.input
question = args.question

# Read input
with open(input_file) as f:
    input = list(f.read().splitlines())

# def parse_input_to_file_system(input):   
#     filesystem = {}
#     dirstack = []
#     current = filesystem

#     for current_line in input:
#         if current_line[0] == "$":
#             if current_line.startswith("$ cd .."):
#                 dirstack.pop()

#                 current = filesystem
#                 for entry in dirstack:
#                     current = filesystem[entry]

#             elif current_line.startswith("$ cd"):
#                 destination = current_line[5:]
#                 if destination == "/":
#                     dirstack = []
#                     current = filesystem
#                 else:
#                     dirstack.append(destination)
#                     current = current[destination]

#         elif current_line.startswith('dir '):
#             dir_name = current_line.split(' ')[1]
#             current[dir_name] = {}
#         else:
#             file_name = current_line.split(' ')[1]
#             file_size = current_line.split(' ')[0]

#             current[file_name] = file_size

#     return filesystem

def parse_input_to_file_system(input):
    file_system = {}
    path = []
    working_directory = file_system

    for line in input:
        if line[0] == "$":
            if line.startswith("$ cd .."):
                # Remove last directory from path
                # Go back to root and go down path again
                # Until we reach parent of the dir we just popped
                path.pop()
                working_directory = file_system
                for dir in path:
                    working_directory = working_directory[dir]
            elif line.startswith("$ cd"):
                destination = line[5:]
                if destination == "/":
                    # Reset to root directory
                    path = []
                    working_directory = file_system
                else:
                    path.append(destination)
                    working_directory = working_directory[destination]

        elif line.startswith('dir '):
            dir_name = line.split(' ')[1]
            working_directory[dir_name] = {}
        else:
            file_name = line.split(' ')[1]
            file_size = line.split(' ')[0]

            working_directory[file_name] = file_size

    return file_system

def find_directory_size(input, current_directory=[], results={}):
    total = 0
    for key, value in input.items():
        if type(value) == str:
            # This is a file
            total = total + int(value)
        else:
            # This is a directory
            current_directory.append(key)
            subtotal = find_directory_size(value, current_directory)['/']
            total = total + subtotal

            path = "/"
            for dir in current_directory:
                path = path + dir + '/'

            results[path] = subtotal
            current_directory.pop()

        results['/'] = total
    return(results)
    


# def find_totals(input):
#     total = 0

#     for key, value in input.items():
#         # File
#         if type(value) == str:
#             total = total + int(value)
#         # Directory
#         else:
#             total = total + find_totals(value)

#             if total <= 100000:
#                 result.append(total)

#     return(total)

# result = []

# Print results depending on the question (1 or 2)
match question:
    case "1":
        file_system = parse_input_to_file_system(input)
        directory_sizes = find_directory_size(file_system)

        result = 0

        for dir, size in directory_sizes.items():
            if size <= 100000:
                result = result + size

        print(result)
    case "2":
        None
