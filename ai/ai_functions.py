import numpy as np
from utility import grid_functions as gf

def select_random_cell(cell_idx_list):
    '''
    This function selects a random game cell.

    @params:
        cell_idx_list - list of cells still in play
    '''
    return np.random.randint(0, len(cell_idx_list))

def select_random_char():
    '''
    This function selects a random game character, S or O.
    '''
    if np.random.randint(2) > 0:
        return b'S'
    return b'O'

def random_move(cell_idx_list):
    '''
    This function makes a random move, both the cell and game character.

    @params:
        cell_idx_list - list of cells still in play

    @returns:
        idx - the index of cell_idx_list, which is the selected game cell
        move - the game character to assign to the selected game cell
    '''
    return select_random_cell(cell_idx_list), select_random_char()

def check_for_good_move(cell_idx_list, game_array, points_list):
    '''
    This function checks to see if a move can be made that awards at least 1 point.
    If no move is found, this function returns an index of -1. If a move is found,
    this function returns the index and game character which will award a point.

    @params:
        cell_idx_list - list of cells still in play
        game_array - character array of game characters in play
        points_list - previously awarded SOS points

    @returns:
        idx - the index of cell_idx_list, which is the selected game cell
        move - the game character to assign to the selected game cell
    '''
    for i in range(0,len(cell_idx_list)):
        temp_array = np.copy(game_array)
        temp_array[cell_idx_list[i]] = b'S'
        new_points, dummy = gf.check_for_sos(temp_array, points_list)
        if new_points > 0:
            return i, b'S'

        #temp_array = np.copy(game_array)
        temp_array[cell_idx_list[i]] = b'O'
        new_points, dummy = gf.check_for_sos(temp_array, points_list)
        if new_points > 0:
            return i, b'O'

    return -1, '-'

def random_safe_move(cell_idx_list, game_array, points_list):
    '''
    This function makes a move which the player will not be able to score
    on their next turn. If no such move is possible, this function returns 
    an index of -1.
    
    @params:
        cell_idx_list - list of cells still in play
        game_array - character array of game characters in play
        points_list - previously awarded SOS points

    @returns:
        idx - the index of cell_idx_list, which is the selected game cell
        move - the game character to assign to the selected game cell
    '''

    safe_idx_list = []
    safe_move_list = []

    # create list of safe moves
    for i in range(0,len(cell_idx_list)):
        temp_array = np.copy(game_array)
        temp_array[cell_idx_list[i]] = b'S'
        idx, move = check_for_good_move(cell_idx_list, temp_array, points_list)
        if idx < 0:
            safe_idx_list.append(i)
            safe_move_list.append(b'S')

        temp_array[cell_idx_list[i]] = b'O'
        idx, move = check_for_good_move(cell_idx_list, temp_array, points_list)
        if idx < 0:
            safe_idx_list.append(i)
            safe_move_list.append(b'O')

    if len(safe_idx_list) > 0:
        idx = select_random_cell(safe_idx_list)
        return safe_idx_list[idx], safe_move_list[idx]

    return -1, '-'
