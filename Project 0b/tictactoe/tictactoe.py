"""
Tic Tac Toe Player
"""

import math,  copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Count the number of X's and O's on the board
    x_count = 0
    y_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                y_count += 1

    # If there are more X's than O's, it's O's turn else it's X's turn
    if x_count > y_count:
        return O
    else:
        return X
    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Initialize an empty set of actions
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if action is valid
    if action not in actions(board):
        raise Exception("Invalid action")
    else:
        # Identify current player
        current_player = player(board)
        # Create deep copy of board
        board_deep_copy =  copy.deepcopy(board)
        # Update board with current player's move
        action_i = action[0]
        action_j = action[1]
        board_deep_copy[action_i][action_j] = current_player
        return board_deep_copy

    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check horizontal rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]
    
    # Check vertical columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
        
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    else:
        return None
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check for winner
    if winner(board) != None:
        return True
    elif EMPTY not in board[0] and EMPTY not in board[1] and EMPTY not in board[2]:
        return True
    else:
        return False
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Check board state for winner
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    # raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check if board is terminal
    if terminal(board):
        return None
    else:
        # Identify current player
        current_player = player(board)
        # Identify possible actions
        possible_actions = actions(board)
        # Check for optimal action
        if current_player == X:
            v = -math.inf
            for action in possible_actions:
                min_value = minimax_min_value(result(board, action))
                if min_value > v:
                    v = min_value
                    optimal_action = action
        else:
            v = math.inf
            for action in possible_actions:
                max_value = minimax_max_value(result(board, action))
                if max_value < v:
                    v = max_value
                    optimal_action = action
        return optimal_action
    # raise NotImplementedError

# Define min_value and max_value helper functions
def minimax_min_value(board):
    # Check if board is terminal
    if terminal(board):
        return utility(board)
    else:
        # Identify possible actions
        possible_actions = actions(board)
        # Initialize v in opposite state
        v = math.inf
        for action in possible_actions:
            max_value = minimax_max_value(result(board, action))
            if max_value < v:
                v = max_value
        return v
    
def minimax_max_value(board):
    # Check if board is terminal
    if terminal(board):
        return utility(board)
    else:
        # Identify possible actions
        possible_actions = actions(board)
        # Initialize v again
        v = -math.inf
        for action in possible_actions:
            min_value = minimax_min_value(result(board, action))
            if min_value > v:
                v = min_value
        return v