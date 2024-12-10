import statistics

with open("input.txt") as f:
    input = f.read().splitlines()


def get_opposite_character(char):
    open_chars = ["(", "[", "{", "<"]
    close_chars = [")", "]", "}", ">"]

    if char in open_chars:
        return close_chars[open_chars.index(char)]
    else:
        return open_chars[close_chars.index(char)]


def is_legitimate_combination(open, close):
    return open == get_opposite_character(close)


def parse_line(line):
    open_chars = ["(", "[", "{", "<"]
    close_chars = [")", "]", "}", ">"]

    opened = []

    for char in line:
        if char in open_chars:
            opened.append(char)
        elif char in close_chars:
            if is_legitimate_combination(opened[-1], char):
                opened.pop()
            else:
                return "corrupted"

    output = []
    for char in reversed(opened):
        output.append(get_opposite_character(char))

    return output


def score_char(char):
    if char == ")":
        return 1
    elif char == "]":
        return 2
    elif char == "}":
        return 3
    elif char == ">":
        return 4


def score_completion_line(completion):
    score = 0
    for char in completion:
        score *= 5
        score += score_char(char)

    return score


results = []
for line in input:
    parse_result = parse_line(line)
    if parse_result == "corrupted":
        None
    else:
        results.append(score_completion_line(parse_result))

results.sort()
print(statistics.median(results))
