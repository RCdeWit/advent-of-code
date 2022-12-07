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
            # Add filesize to total
            total = total + int(value)
        else:
            # This is a directory
            # Go one level deeper
            current_directory.append(key)

            # Recursively search directory
            subtotal = find_directory_size(value, current_directory)['/']
            total = total + subtotal

            # Create distinct keys based on full paths
            path = "/"
            for dir in current_directory:
                path = path + dir + '/'

            results[path] = subtotal

            # Go back to parent directory
            current_directory.pop()

        # Save total
        results['/'] = total

    return(results)

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
        file_system = parse_input_to_file_system(input)
        directory_sizes = find_directory_size(file_system)

        # Calculate space needed for update
        current_space_available = 70000000 - directory_sizes['/']
        space_needed = 30000000
        space_to_clear = space_needed - current_space_available

        # Identify possible directories for deletion
        candidates_for_deletion = {}
        for dir, size in directory_sizes.items():
            if size >= space_to_clear:
                candidates_for_deletion[dir] = size

        # Keep the smallest one as result
        print(min(candidates_for_deletion.values()))
