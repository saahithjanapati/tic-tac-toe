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

def game_over_nega(board_string, token):
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
                if symbol == token:
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
                if symbol == token:
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
            if symbol == token:
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
            if symbol == token:
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
    board_copy = str(board_string)
    index = find_index(board_copy, ".")
    while index != -1:
        move_set.add(index)
        board_copy = board_copy[0:index] + max_symbol + board_copy[index+1:]
        index = find_index(board_copy, ".")
    return move_set



def make_move(board, move, token):
    """modifies board to include token at move specified"""
    board = board[0:move] + token + board[move+1:]

def unmake_move(board, move):
    """modifies board to remove token at move specified"""
    board = board[0:move] + "." + board[move+1:]


def get_other_token(token):
    """returns opposing player's token"""
    if token == "X": return "O"
    else: return "X"

#NEGAMAX
def negamax(board, token):
    """negamax function"""
    result = game_over_nega(board, token)
    print(result)
    if result in [-1,0,1]:
        return result, -1
    index = -1
    score = 1
    other_token = get_other_token(token)
    for move in get_possible_moves(board):
        make_move(board, move, other_token)
        val = -1 * negamax(board, other_token)[0]
        unmake_move(board, move)
        if val < score:
            score = val
            index = move
    return score, index


def negamax_helper(token, board):
    """a helper method for negamax to talk with old code
    creates a play_dict, containing move values as keys and
    their values as the values of the dictionary"""
    best_move = None
    play_dict = {}
    for move in sorted(list(get_possible_moves(board))):
        make_move(board, move, token)
        new_score = negamax(board, token)
        unmake_move(board, move)
        play_dict[move] = new_score
    return play_dict


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


def play_turn(board_string):
    # play_dict = negamax_helper(max_symbol, board_string)
    best_move = negamax(max_symbol, board_string)
    print(best_move)
    # best_move = list(play_dict.keys())[0]
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
        print("\n")
        print(print_game(board_string))
        print("\n")
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
