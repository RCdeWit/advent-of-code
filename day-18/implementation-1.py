# import ast
# import math
#
# with open('example-input.txt') as f:
#     input = f.read().splitlines()
#
# list_of_numbers = []
#
# for line in input:
#     list_of_numbers.append(ast.literal_eval(line))
#
# def add_snailfish_numbers(number1, number2):
#     return [number1, number2]
#
# def split_number(number):
#     stringified = str(number).replace(" ", "")
#
#     output = ""
#     for c, char in enumerate(stringified):
#         if char.isnumeric():
#             if stringified[c+1].isnumeric():
#                 split = int(stringified[c:c+1])
#                 value1 = str(math.floor(split / 2))
#                 value2 = str(math.ceil(split / 2))
#
#                 output += "[" + str(value1) + "," + str(value2) + "]"
#                 output += stringified[c+2:]
#                 return ast.literal_eval(output)
#             else:
#                 output += char
#         else:
#             output += char
#
#     return ast.literal_eval(output)
#
# def explode_number(number):
#     value1 = number[0]
#     value2 = number[1]
#
#     numbers = {}
#     depth = 0
#     stringified = str(number).replace(" ", "")
#
#     position = 0
#     number_to_add = ""
#     depth_at_number = 0
#     is_left_number = False
#     while len(stringified) > 0:
#         if stringified[0] == "[":
#             depth += 1
#             is_left_number = True
#         elif stringified[0] == "]":
#             depth -= 1
#         elif stringified[0].isnumeric():
#             number_to_add += stringified[0]
#             depth_at_number = depth
#         elif stringified[0] == ",":
#             entry = {}
#             entry["position"] = len(numbers)
#             entry["value"] = int(number_to_add)
#             entry["depth"] = depth_at_number
#             entry["is_left_number"] = is_left_number
#
#             numbers[len(numbers)] = entry
#             number_to_add = ""
#             is_left_number = False
#
#         stringified = stringified[1:]
#
#     # Add last number that isn't followed by comma
#     entry = {}
#     entry["position"] = len(numbers)
#     entry["value"] = int(number_to_add)
#     entry["depth"] = depth_at_number
#     entry["is_left_number"] = is_left_number
#     numbers[len(numbers)] = entry
#
#     # Do the explosion
#     for number in numbers:
#         number = numbers[number]
#
#         if number["depth"] == 5:
#             i = number["position"]
#             if i == 0:
#                 None
#             else:
#                 value_to_left = numbers[i-1]
#                 value_to_left["value"] = value_to_left["value"] + number["value"]
#                 numbers[i-1] = value_to_left
#
#             paired_number = numbers[number["position"]+1]
#             j = paired_number["position"]
#             if j == len(numbers) - 1:
#                 None
#             else:
#                 value_to_right = numbers[j+1]
#                 value_to_right["value"] = value_to_right["value"] + paired_number["value"]
#                 numbers[j+1] = value_to_right
#
#             new_number = number
#             new_number["value"] = 0
#             new_number["depth"] -= 1
#             numbers[i] = new_number
#             del(numbers[j])
#
#             break
#
#     # print(numbers)
#     # quit()
#
#     # Format back to output
#     output = ""
#     current_depth = 0
#     for number in numbers:
#         number = numbers[number]
#         while current_depth < number["depth"]:
#             if len(output) > 0 and output[-1].isnumeric():
#                 output += ","
#             output += "["
#             current_depth += 1
#         while current_depth > number["depth"]:
#             output += "]"
#             current_depth -= 1
#
#         if output[-1].isnumeric():
#             output += ","
#             output += str(number["value"])
#         elif output[-1] == "]":
#             if number["is_left_number"]:
#                 output += "],["
#             else:
#                 output += ","
#             output += str(number["value"])
#
#         else:
#             output += str(number["value"])
#
#     for i in range(current_depth):
#         output += "]"
#
#     return ast.literal_eval(output)
#
# def reduce_number(number):
#     output = explode_number(number)
#     if output != number:
#         return output
#     else:
#         return split_number(number)
#
# def process_reduction(number):
#     last_iteration = number
#     output = None
#
#     while True:
#         output = reduce_number(last_iteration)
#         if last_iteration == output:
#             break
#         else:
#             last_iteration = output
#
#     return output
#
# # result = []
# # for number in list_of_numbers:
# #     if len(result) == 0:
# #         result = number
# #     else:
# #         result = add_snailfish_numbers(result, number)
# #
# #     result = process_reduction(result)
# #
# # print(result)
#
# # print(reduce_snailfish_number(list_of_numbers[0]))
#
# # print(process_reduction(list_of_numbers[5]))
# print(reduce_number(list_of_numbers[5]))
# #
# # [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
# # [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
