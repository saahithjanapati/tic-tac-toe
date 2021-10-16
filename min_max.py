import sys

max_symbol = "X"
min_symbol = "O"


def string_to_matrix(board_string):
    matrix = []
    for x in range(3):
        new_row = []
        for y in range(3):
            new_row.append(board_string[3*x+y])
        matrix.append(new_row)
    return matrix


# print(string_to_matrix("........."))
def game_over(board_string):
    """returns info about game
    if game is not over, returns False
    if x won, return 1
    if o won return -1
    if tie return 0
    """

    board = string_to_matrix(board_string)
    space_is_empty = False


    # checking rows
    for row in range(3):
        symbol = board[row][0]
        if symbol == ".": space_is_empty = True
        else:
            row_won = True
            for col in range(1,3):
                if board[row][col] != symbol:
                    row_won = False
            if row_won:
                if symbol == max_symbol:
                    return 1
                else:
                    return -1

    # checking columns
    for col in range(3):
        symbol = board[0][col]
        if symbol == ".": space_is_empty = True
        else:
            col_won = True
            for row in range(1,3):
                if board[row][col] != symbol:
                    col_won = False
            if col_won:
                if symbol == max_symbol:
                    return 1
                else:
                    return -1

    # checking diagonals
    symbol = board[0][0]
    if symbol == ".": space_is_empty = True
    else:
        diagonal_won = True
        start_row = 1
        start_col = 1
        for i in range(0, 2):

            if board[start_row + i][start_col + i] != symbol:
                diagonal_won = False
        if diagonal_won:
            if symbol == max_symbol:
                return 1
            else:
                return -1

    symbol = board[0][2]
    if symbol == ".": space_is_empty = True
    else:
        diagonal_won = True
        start_row = 1
        start_col = 1
        for i in range(0, 2):
            if board[start_row + i][start_col - i] != symbol:
                diagonal_won = False
        if diagonal_won:
            if symbol == max_symbol:
                return 1
            else:
                return -1

    tied = True
    for row in range(3):
        for col in range(3):
            if board[row][col] == ".":
                tied = False
    if tied: return 0
    return False


def find_index(board_string, char):
    for i in range(len(board_string)):
        if board_string[i] == char:
            return i
    return -1


def get_possible_moves(board_string):
    move_set = set()

    index = find_index(board_string, ".")
    while index != -1:
        move_set.add(index)
        board_string = board_string[0:index] + max_symbol + board_string[index+1:]
        index = find_index(board_string, ".")
    return move_set


def max_play(board_string):
    game_over_output = game_over(board_string)
    if game_over_output is not False:
        return game_over_output
    else:
        move_set = get_possible_moves(board_string)
        max_value = -1
        for move in move_set:
            new_board_string  = board_string[0:move] + max_symbol + board_string[move+1:]
            val = min_play(new_board_string)
            if val > max_value:
                max_value = val
        return max_value


def min_play(board_string):
    game_over_output = game_over(board_string)
    if game_over_output is not False:
        return game_over_output
    else:
        move_set = get_possible_moves(board_string)
        min_value = 1
        for move in move_set:
            new_board_string = board_string[0:move] + min_symbol + board_string[move+1:]
            val = max_play(new_board_string)
            if val < min_value:
                min_value = val
        return min_value


def print_game(board_string):
    matrix = string_to_matrix(board_string)
    output_string = "Current board:\n"
    for row in range(0,3):
        number_string = ""
        for col in range(0,3):
            output_string += matrix[row][col]
            number_string += str(row*3+col)
        output_string += "    "
        output_string += number_string + "\n"
    return output_string[0:len(output_string)-1]


def calculate_all_moves(board_string):
    move_set = get_possible_moves(board_string)
    play_dict = dict()
    for move in move_set:
        new_board_string = board_string[0:move] + max_symbol + board_string[move+1:]
        play_dict[move] = min_play(new_board_string)
    return play_dict


def play_turn(board_string):
    play_dict = calculate_all_moves(board_string)
    best_move = list(play_dict.keys())[0]
    for move in play_dict.keys():
        if play_dict[move] == 0:
            game_result = "tie"
        elif play_dict[move] == -1:
            game_result = "loss"
        else:
            game_result = "win"
        print("Moving at " + str(move) + " results in a " + game_result + ".")
        if play_dict[move] > play_dict[best_move]:
            best_move = move

    print()
    print("I chose space " + str(best_move) + ".")
    new_board_string = board_string[0:best_move] + max_symbol + board_string[best_move+1:]
    return new_board_string


def main():
    global max_symbol, min_symbol
    board_string = sys.argv[1]
    if find_index(board_string, "X") == -1 and find_index(board_string, "O") == -1:
        max_symbol = input("Should I be X or O? ")
        if max_symbol == "X":
            computer_turn = True
        else:
            min_symbol = "X"
            computer_turn = False
    else:       # player is giving partially filled in board
        computer_turn = True

        x_count = board_string.count("X")
        o_count = board_string.count("O")
        # it's always the computer's turn in this else block
        if x_count == o_count:
            max_symbol = "X"
        elif o_count > x_count:
            max_symbol = "X"
        else:
            max_symbol = "O"
            min_symbol = "X"

    while game_over(board_string) is False:
        print()
        print(print_game(board_string))
        print()
        if computer_turn:
            board_string = play_turn(board_string)
        else:
            poss_moves = get_possible_moves(board_string)
            output = "You can move to any of these spaces: "
            for move in poss_moves:
                output += str(move) + ", "
            output = output[0:len(output)-2] + "."
            print(output)
            human_move_index = int(input("Your choice? "))
            board_string = board_string[0:human_move_index] + min_symbol + board_string[human_move_index+1:]
        computer_turn = not computer_turn

    print()
    print(print_game(board_string))
    print()
    game_state = game_over(board_string)
    if game_state == 0:
        print("We tied!")
    else:
        print("I win!")

if __name__ == "__main__":
    main()
