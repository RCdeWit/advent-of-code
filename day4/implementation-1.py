# First process input data
with open('input.txt') as f:
    input = f.read().splitlines()

# Save input to list of balls and remove from bingo cards to be processed
balls = list(map(int, input[0].split(",")))
input = input[2:]

# Remove double spaces as seperators for numbers <10
# If first number in row is <10, remove first character (space)
temp_input = []
for line in input:
    new_line = line.replace("  ", " ")

    # This is needed to prevent out of index errors on empty lines.
    try:
        if new_line[0] == " ":
            new_line = new_line[1:]
    except:
        None

    temp_input.append(new_line)
input = temp_input

# Process data into bingo card arrays
list_of_cards = []
card = []

for i, line in enumerate(input):
    if line == "":
        # Write to list of cards upon new line
        list_of_cards.append(card)
        card = []
    else:
        row = list(map(int, input[i].split(" ")))
        card.append(row)
# Append last card without trailing new line
list_of_cards.append(card)

# Function to cross off a number on a bingo card
def cross_off_number(bingo_card, number):
    for i, row in enumerate(bingo_card):
        for j, cell in enumerate(row):
            if bingo_card[i][j] == number:
                bingo_card[i][j] = -1

    return bingo_card

# Function to check whether a given card gets a bingo
def check_bingo_card(bingo_card):
    n_row = len(bingo_card)
    n_col = len(bingo_card[0])
    bingo_row = [True] * n_row
    bingo_col = [True] * n_col

    for c in range(n_col):
        for r in range(n_row):
            if bingo_card[r][c] != -1:
                bingo_row[c] = False
                bingo_col[r] = False

    # If one of the rows or columns is still true, it's a bingo!
    return max(bingo_row) or max(bingo_col)
#
# test_card_row = [[-1, -1, -1, -1, -1], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]]
# test_card_col = [[22, -1, 17, 11, 0], [8, -1, 23, 4, 24], [21, -1, 14, 16, 7], [6, -1, 3, 18, 5], [1, -1, 20, 15, 19]]
# print(check_bingo_card(test_card_row, test_card_col))

def sum_remaining_cells(bingo_card):
    sum = 0
    n_row = len(bingo_card)
    n_col = len(bingo_card[0])

    for c in range(n_col):
        for r in range(n_row):
            if bingo_card[r][c] != -1:
                sum += bingo_card[r][c]

    return sum


for b in range(len(balls)):
    for c in range(len(list_of_cards)):
        list_of_cards[c] = cross_off_number(list_of_cards[c], balls[b])

        if check_bingo_card(list_of_cards[c]):
            print(f"Last ball: {balls[b]}, Remainder card: {sum_remaining_cells(list_of_cards[c])}")
            print(f"Answer: {balls[b] * sum_remaining_cells(list_of_cards[c])}")
            exit()
