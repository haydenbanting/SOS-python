import numpy as np
from config import constants as c

def create_game_array(x_cells=c.GAME_GRID_W, y_cells=c.GAME_GRID_H):
    '''
    This function produces the game array, which is a 2D character array
    where all entries are initially populated by default with the 
    character '-'.

    @params:
        x_cells - number of columns in array
        y_cells - number of rows in array

    @returns:
        game_array - 2D character array used for storing game moves
    '''
    game_array = np.chararray((x_cells, y_cells))
    game_array[:] = '-'
    return game_array

def check_for_grid_click(pos, cell_rect_list):
    '''
    This function if a cell was clicked, and if so returns the index of
    corresponding cell.

    @params:
        pos - mouse position (x,y)
        cell_rect_list - list of game cell hitboxes
    '''
    for i in range(0,len(cell_rect_list)):
        if cell_rect_list[i].collidepoint(pos):
            return i
    return  -1

def check_for_sos(game_array, points_list):
    '''
    This function checks the game array if a new SOS has been made.

    @params:
        game_array - 2D character array with game moves
        points_list - list of coordinates which previous SOS points have been awarded

    @returns:
        num_points - number of points to be awarded (new SOS)
        new_points_list - new SOS coordinates, which points should not be awarded on subsequent checks
    '''
    num_rows, num_cols = game_array.shape

    num_points = 0
    new_points_list = []

    # check top row
    for i in range(0,num_cols-2):
        if game_array[(0,i)] == b'S':
            if game_array[(0,i+1)] == b'O':
                if game_array[(0,i+2)] == b'S':
                    if [(0,i), (0,i+1), (0,i+2)] not in points_list:
                        num_points += 1
                        new_points_list.append([(0,i), (0,i+1), (0,i+2)])

    # check bot row
    for i in range(0,num_cols-2):
        if game_array[(num_rows-1,i)] == b'S':
            if game_array[(num_rows-1,i+1)] == b'O':
                if game_array[(num_rows-1,i+2)] == b'S':
                    if [(num_rows-1,i), (num_rows-1,i+1), (num_rows-1,i+2)] not in points_list:
                        num_points += 1
                        new_points_list.append([(num_rows-1,i), (num_rows-1,i+1), (num_rows-1,i+2)])

    # check outer left row
    for i in range(0,num_rows-2):
        if game_array[(i,0)] == b'S':
            if game_array[(i+1,0)] == b'O':
                if game_array[(i+2,0)] == b'S':
                    if [(i,0), (i+1,0), (i+2,0)] not in points_list:
                        num_points += 1
                        new_points_list.append([(i,0), (i+1,0), (i+2,0)])

    # check right row
    for i in range(0,num_rows-2):
        if game_array[(i,num_cols-1)] == b'S':
            if game_array[(i+1,num_cols-1)] == b'O':
                if game_array[(i+2,num_cols-1)] == b'S':
                    if [(i,num_cols-1), (i+1,num_cols-1), (i+2,num_cols-1)] not in points_list:
                        num_points += 1
                        new_points_list.append([(i,num_cols-1), (i+1,num_cols-1), (i+2,num_cols-1)])

    # check all other rows
    for i in range(1,num_rows-1):
        for j in range(1,num_cols-1):
            if game_array[(i,j)] == b'O':
                if game_array[(i-1,j-1)] == b'S' and game_array[(i+1,j+1)] == b'S': # left diag
                    if [(i-1,j-1), (i,j), (i+1,j+1)] not in points_list:
                        num_points += 1
                        new_points_list.append([(i-1,j-1), (i,j), (i+1,j+1)])
                if game_array[(i-1,j+1)] == b'S' and game_array[(i+1,j-1)] == b'S': # right diag
                    if [(i-1,j+1), (i,j), (i+1,j-1)] not in points_list:
                        num_points += 1
                        new_points_list.append([(i-1,j+1), (i,j), (i+1,j-1)])
                if game_array[(i-1,j)] == b'S' and game_array[(i+1,j)] == b'S': # vertical
                    if [(i-1,j), (i,j), (i+1,j)] not in points_list:
                        num_points += 1
                        new_points_list.append([(i-1,j), (i,j), (i+1,j)])
                if game_array[(i,j-1)] == b'S' and game_array[(i,j+1)] == b'S': # horizontal
                    if [(i,j-1), (i,j), (i,j+1)] not in points_list:
                        num_points += 1
                        new_points_list.append([(i,j-1), (i,j), (i,j+1)])

    return num_points, new_points_list