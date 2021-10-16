#variables to configure
depth = 5

possible_wins = [(0,1,2), (3,4,5), (6,7,8), #horizontal wins
                 (0,3,6), (1,4,7), (2,5,8), #vertical wins
                 (0,4,8), (2,4,6)]
master_board = ["."]*9    # state of larger tic-tac-toe board
token_list = ["X", "O"]
ALPHA_START = -1e30000
BETA_START = 1e30000

def convert_coordinate_to_index(row, col):
    return (int(row/3)*27) + int(col/3)*9 + int(row%3)*3 + col%3


def convert_coordinate_to_box(row, col):
    index = convert_coordinate_to_index(row, col)
    return index % 9


def print_game(state):
    return_string = "   0 1 2  3 4 5  6 7 8\n"
    for i in range(9):
        if i%3 == 0:
            return_string += "   " + "-" * 20 + "\n"
        return_string += str(i) + " "
        for j in range(9):
            if j % 3 == 0:
                return_string += "|"
            return_string += state[convert_coordinate_to_index(i, j)] + " "
        return_string += "|\n"
    return_string += "   " + "-" * 20 + "\n"
    return return_string


def get_small_board(state, board_num):
    small_board_string = ""
    starting_index = board_num*9
    for i in range(0, 9):
        # print(state[starting_index+1])
        small_board_string += state[starting_index+i]
    return small_board_string


def heuristic_helper(small_board_string, token):
    score = 0

    for win_config in possible_wins:
        count = 0
        for index in win_config:
            if small_board_string[index] == token: count += 1
        if count == 3:
            score += 100
        elif count == 2:
            score += 10
        elif count == 1:
            score += 1
    return score

def heuristic(state, bigboard, token):
    """evaluation function for negamax
    evaluates from perspective of player
    passed in argument

    will take into account incomplete boards and complete boards
    (using master_board)
    """
    total_score = 0
    total_score += heuristic_helper(bigboard, token) * 100
    for i in range(0,9):
        total_score += heuristic_helper(get_small_board(state, i), token)
    return total_score


def possible_moves(state, big_board, last_move):
    """returns list of indices where computer can play"""
    # print(state)
    # print(big_board)
    possible_indices = []
    if big_board[last_move] != ".": #all open because last_move box is filled up
        for i in range(len(state)):
            if state[i] == ".":
                possible_indices.append(i)
    else:
        list = []
        starting_index = last_move*9
        for i in range(0, 9):
            list.append(starting_index+i)
        for index in list:
            if state[index] == ".":
                possible_indices.append(index)
    return possible_indices



def negamax(state, big_board, last_move, depth, alpha, beta, token):
    if depth == 0:
        return heuristic(state, big_board, token)
    result = game_over(token, big_board)
    if result == 1:
        return BETA_START
    if result == -1 or 0:
        return ALPHA_START
    move_set = possible_moves(state, big_board, last_move)
    value = ALPHA_START
    for index in move_set:
        child_state = place_token(state, -1, -1, token, index)
        child_master_board = update_master_board(child_state)
        child_last_move = index%9
        nega_val = -negamax(child_state, child_master_board, child_last_move, depth-1, -beta, -alpha, get_opp_token(token))
        value = max(value, nega_val)
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return alpha



def play_computer_turn(state, computer_token, last_move):
    """plays computer turn"""
    # play_computer_turn(state, board_open, computer_token, last_move)
    global depth
    big_board = update_master_board(state)
    play_dict = {}
    if len(possible_moves(state, big_board, last_move)) < 9:
        temp_depth = 1
    else:
        temp_depth = depth
    for index in possible_moves(state, big_board, last_move):
        child_state = place_token(state, -1, -1, computer_token, index)
        child_master_board = update_master_board(child_state)
        child_last_move = index%9
        nega_val = -1 * negamax(child_state, child_master_board, child_last_move, temp_depth, ALPHA_START, BETA_START, get_opp_token(computer_token))
        play_dict[index] = nega_val

    best_key = list(play_dict.keys())[0]
    for key in play_dict.keys():
        if play_dict[key] > play_dict[best_key]:
            best_key = key
    new_state = place_token(state, -1, -1, computer_token, best_key)
    return new_state, best_key%9


def get_opp_token(token):
    if token == "O": return "X"
    return "O"

def game_over(token, board):
    """checks if game is over"""
    """returns 1 if token won game, -1 if opp won gamve"""
    for win_tuple in possible_wins: #defined above
        if board[win_tuple[0]] == board[win_tuple[1]] == board[win_tuple[2]]:
            if board[win_tuple[0]] == token:
                return 1
            if board[win_tuple[0]] == get_opp_token(token): return -1
    if "." in board: return 2 #not complete
    return 0 #draw


def small_board_filled(state, board_num):
    """returns true if small_board (specified by board_num) is filled
    false otherwise
    """
    small_board_string = get_small_board(state, board_num)
    return not ("." in small_board_string)



def valid_check(row, col, state, square):
    converted_index = convert_coordinate_to_index(row, col)
    if row < 9 and col < 9:
        starting_index = square*9
        list = []
        for i in range(0, 9):
            list.append(starting_index+i)
        if converted_index not in list or state[converted_index] != ".": return False
        return True
    return False


def place_token(state, row, col, token, index=-1):
    """places token in given row and col
    returns updated state"""
    if index == -1: index = convert_coordinate_to_index(row, col)
    new_state = state[:index] + token + state[index+1:]
    return new_state



def play_human_turn(state, board_open, token, last_move):
    playable_squares = []
    print(print_game(state))
    if board_open:
        for i in range(len(master_board)):
            if master_board[i] == ".":
                playable_squares.append(i)
    else:
        playable_squares.append(last_move)
    print("Squares: ")
    print("0 1 2\n3 4 5\n6 7 8\n")
    if len(playable_squares) > 1:

        print("Which square would you like to play in?")
        print("Your possible options are: " + str(playable_squares))
        square = int(input("Square: "))
        while square not in playable_squares:
            print("Your possible options are: " + str(playable_squares))
            square = int(input("Square: "))
    else:
        square = playable_squares[0]

    print("You are playing in Square: " + str(square))
    valid = False
    while not valid:
        row = int(input("Input the row you would like to play in: "))
        col = int(input("Input the column you would like to play in: "))

        if valid_check(row, col, state, square):
            valid = True
        if not valid: print("Invalid move!")
    state = place_token(state, row, col, token)
    converted_index = convert_coordinate_to_index(row, col)
    last_move = converted_index%9
    return state, last_move



def update_master_board(state):
    # global master_board
    for i in range(9):
        small_board_string = get_small_board(state, i)
        result = game_over("X", small_board_string)
        indices = []
        starting_index = i*9
        for j in range(0, 9):
            # print(state[starting_index+1])
            indices.append(starting_index+j)

        if result == 2:
            master_board[i] = "."
        if result == 1:
            master_board[i] = "X"
            for index in indices:
                state = place_token(state, -1, -1, "X", index)
                # print(state)
        elif result == -1:
            master_board[i] = "O"
            for index in indices:
                state = place_token(state, -1, -1, "O", index)
        elif result == 0:
            master_board[i] = "/"
            for index in indices:
                state = place_token(state, -1, -1, "/", index)
    return master_board


def test():
    global master_board
    state = "X.....OOO" + "." * 72
    print(state)
    small_board = get_small_board(state, 0)
    print(small_board)
    print(game_over("X", get_small_board(state, 0)))


def main():
    global master_board
    state = "."*81
    human_token = input("Would you like to be O or X? ")
    while human_token not in token_list:
        human_token = input("Please enter either O or X: ")
    computer_token = token_list[not token_list.index(human_token)]
    computer_turn = human_token != "X"
    board_open = True
    last_move = None

    while game_over(computer_token, master_board) == 2:
        if computer_turn:
            state, last_move = play_computer_turn(state, computer_token, last_move)
        else:
            state, last_move = play_human_turn(state, board_open, human_token, last_move)
        computer_turn = not computer_turn
        master_board = update_master_board(state)
        board_open = not(master_board[last_move] == ".")
        print(master_board)
        print("Last move: " + str(last_move))
        print("Board Open: " + str(board_open))


    result = game_over(state, computer_token)
    if result == -1:
        print("You won!")
    elif result == 1:
        print("I won!")
    else:
        print("Tie game!")


main()
