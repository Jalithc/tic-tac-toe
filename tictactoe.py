import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):

    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)
    if count_x > count_o:
        return O
    else:
        return X


def actions(board):

    Allposibilities = set()

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                Allposibilities.add((row, col))
    return Allposibilities


def result(board, action):

    if action not in actions(board):
        raise Exception("Not valid action")
    row, col = action
    board_copy = copy.deepcopy(board)
    board_copy[row][col] = player(board)
    return board_copy


def checkRow(board, player):
    for row in range(len(board)):
        if all(cell == player for cell in board[row]):
            return True
    return False


def checkCol(board, player):
    for col in range(len(board[0])):
        if all(board[row][col] == player for row in range(len(board))):
            return True
    return False


def checkFirstDig(board, player):
    return all(board[i][i] == player for i in range(len(board)))


def checkSecondDig(board, player):
    return all(board[i][len(board)-i-1] == player for i in range(len(board)))


def winner(board):

    for player in [X, O]:
        if checkRow(board, player) or checkCol(board, player) or checkFirstDig(board, player) or checkSecondDig(board, player):
            return player
    return None


def terminal(board):

    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def minimax(board):

    if terminal(board):
        return None

    if player(board) == X:
        v = -math.inf
        best_action = None
        for action in actions(board):
            min_val = min_value(result(board, action))
            if min_val > v:
                v = min_val
                best_action = action
        return best_action

    elif player(board) == O:
        v = math.inf
        best_action = None
        for action in actions(board):
            max_val = max_value(result(board, action))
            if max_val < v:
                v = max_val
                best_action = action
        return best_action