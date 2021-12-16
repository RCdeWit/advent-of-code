with open('input.txt') as f:
    input = f.read().splitlines()

def decode_hex_to_binary(string):
    output = ""

    for char in string:
        if char == "0":
            output += "0000"
        elif char == "1":
            output += "0001"
        elif char == "2":
            output += "0010"
        elif char == "3":
            output += "0011"
        elif char == "4":
            output += "0100"
        elif char == "5":
            output += "0101"
        elif char == "6":
            output += "0110"
        elif char == "7":
            output += "0111"
        elif char == "8":
            output += "1000"
        elif char == "9":
            output += "1001"
        elif char == "A":
            output += "1010"
        elif char == "B":
            output += "1011"
        elif char == "C":
            output += "1100"
        elif char == "D":
            output += "1101"
        elif char == "E":
            output += "1110"
        elif char == "F":
            output += "1111"

    return(output)

def split_packages(binary, threshold, mode="total_length_subpackets"):
    output = []
    package_1 = extract_information_from_binary(binary)

    position = package_1["length"]
    output.append(package_1)

    remaining_binary = binary[position:]

    if mode == "total_length_subpackets":
        while position < threshold: # HIER GAAT IETS MIS
            package_n = extract_information_from_binary(remaining_binary)
            output.append(package_n)
            position += package_n["length"]
            remaining_binary = binary[position:]

    elif mode == "number_of_subpackets":
        while len(output) < threshold:
            package_n = extract_information_from_binary(remaining_binary)
            output.append(package_n)
            position += package_n["length"]
            remaining_binary = binary[position:]

    return output

def extract_information_from_binary(binary):
    output = {}

    version = int(binary[0:3], 2)
    type = int(binary[3:6], 2)

    output["version"] = version
    output["type"] = type
    # output["length"] = None

    position = 6

    # Literal value
    if type == 4:
        value = ""
        position_in_group = 0
        last_group = False
        for d in range(position, len(binary)):
            # Read if this is the last group yet
            if position_in_group == 0:
                last_group = binary[d] == "0"
            # Add group digits to value
            else:
                value += binary[d]

            # Move through position (absolute and relative to group)
            position += 1
            position_in_group += 1

            # Set new group once we hit the end
            if position_in_group > 4:
                position_in_group = 0

            # If we just processed the last group, we can disregard the rest
            if position_in_group == 0 and last_group:
                break

        output["value"] = int(value, 2)

    # Operator
    else:
        length_type_id = int(binary[6], 2)

        if length_type_id == 0:
            total_length_subpackets = int(binary[7:22], 2)
            output["total_length_subpackets"] = total_length_subpackets
            position = 22
            output["subpackets"] = split_packages(binary[position:position+total_length_subpackets], total_length_subpackets, mode="total_length_subpackets")
            position += total_length_subpackets

        elif length_type_id == 1:
            number_of_subpackets = int(binary[7:18], 2)
            output["number_of_subpackets"] = number_of_subpackets
            position = 18
            output["subpackets"] = split_packages(binary[position:], number_of_subpackets, mode="number_of_subpackets")

            for s in output["subpackets"]:
                position += s["length"]

    output["length"] = position
    return output

def sum_version_numbers(dictionary):
    sum = 0
    versions = []

    sum += dictionary["version"]
    versions.append(dictionary["version"])

    if "subpackets" in dictionary:
        for subpacket in dictionary["subpackets"]:
            sub = sum_version_numbers(subpacket)[0]
            sum += sub
            versions.append(sub)

    return [sum, versions]


example = input[0]
binary = decode_hex_to_binary(example)

result = extract_information_from_binary(binary)

print(sum_version_numbers(result))
