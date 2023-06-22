"""
Tic Tac Toe Player
"""

import copy
import math

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
    x_count = 0
    o_count = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                o_count += 1

    if o_count < x_count:
        return O
    else:
        return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return_set = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return_set.append((i, j))
    #print(return_set)
    return set(return_set)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Create new board, without modifying the original board received as input
    board_cpy = copy.deepcopy(board)

    board_cpy[action[0]][action[1]] = player(board)
    return board_cpy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #Check Hoirrizontally for X
    for i in range(3):
        ok_x = 1
        for j in range(3):
            #print(board)
            if board[i][j] == X:
                continue
            else:
                ok_x = 0
                break
    
        if ok_x:
            return X
    
    #Check Vertically for X
    for j in range(3):
        ok_x = 1
        for i in range(3):
            if board[i][j] == X:
                continue
            else:
                ok_x = 0
                break
        if ok_x:
            return X
        
    #Check Diagonally(1) for X
    ok_x = 1
    for i in range(3):
        if board[i][i] == X:
            continue
        else:
            ok_x = 0
            break
    if ok_x:
        return X
    
    #Check Diagonally(2) for X
    ok_x = 1
    j = 2
    for i in range(3):
        if board[i][j] == X:
            j -= 1
            continue
        else:
            ok_x = 0
            break
    if ok_x:
        return X


    #Check Hoirrizontally for O
    for i in range(3):
        ok_y = 1
        for j in range(3):
            if board[i][j] == O:
                continue
            else:
                ok_y = 0
                break
    
        if ok_y:
            return O
    
    #Check Vertically for O
    for j in range(3):
        ok_y = 1
        for i in range(3):
            if board[i][j] == O:
                continue
            else:
                ok_y = 0
                break
        if ok_y:
            return O
        
    #Check Diagonally(1) for O
    ok_y = 1
    for i in range(3):
        if board[i][i] == O:
            continue
        else:
            ok_y = 0
            break
    if ok_y:
        return O
    
    #Check Diagonally(2) for O
    ok_y = 1
    j = 2
    for i in range(3):
        if board[i][j] == O:
            j -= 1
            continue
        else:
            ok_y = 0
            break
    
    if ok_y:
        return O


    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #print(board, "win")
    win = winner(board)
    if win:
        return True
    
    empty = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                empty = 1
                break
        if empty:
            break
    if not empty:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    
    else:
        return 0


def Min_Value(board):
    if terminal(board):
        return utility(board), None


    v =  9999999999999
    ret_action = None
    list_actions = list(actions(board))
    for action in list_actions:
        #print(action, list_actions)
        v_temp, action_temp = Max_Value(result(board, action))
        if v_temp < v:
            v = v_temp
            ret_action = action
            if v == -1:
                return v, ret_action
            
    return v, ret_action
 

def Max_Value(board):
    if terminal(board):
        return utility(board), None
    
    v = -9999999
    ret_action = None
    for action in list(actions(board)):
#        print('list: ',action, list(actions(board)))
        v_temp, action_temp = Min_Value(result(board, action))
        if v_temp > v:
            ret_action = action
            v = v_temp
            if v == 1:
                return v, ret_action
    return v, ret_action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    current_player = player(board)
    if current_player == X:
        v, act_temp = Max_Value(board)
        #print(act_temp, "act_temp")
        return act_temp
    elif current_player == O:
        v, act_temp = Min_Value(board)
        #print("act_temp", act_temp)
        return act_temp

    
