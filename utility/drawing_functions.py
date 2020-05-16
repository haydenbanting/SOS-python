import pygame
import numpy as np
from config import constants as c

def draw_grid(screen, x_cells=c.GAME_GRID_W, y_cells=c.GAME_GRID_H):
    '''
    This function draws the game grid.

    @params:
        screen - pygame object to draw on
        x_cells - number of game columns
        y_cells - number of game rows

    @returns:
        cell_rect_list - a list of hitboxes for each game cell drawn
        cell_idx_list - list of indexes which map hitboxes in cell_rect_list to the 2D game char array
    '''

    # Compute total game size area, center it
    x_size = x_cells*c.GAME_CELL_W
    y_size = y_cells*c.GAME_CELL_H
    game_area = pygame.Rect(0, 0, x_size, y_size)
    game_area.center = (c.RESOLUTION_WIDTH / 2, c.RESOLUTION_HEIGHT/2)

    # where to start drawing
    x_pos = game_area.left
    y_pos = game_area.top
    cell_rect_list = []
    cell_idx_list = []
    

    for i in range(0,y_cells):
        for j in range(0,y_cells):
            pygame.draw.rect(screen, (10*i,20*j,10*i), (x_pos, y_pos, c.GAME_CELL_W, c.GAME_CELL_H), 3)
            cell_rect_list.append(pygame.Rect(x_pos, y_pos, c.GAME_CELL_W, c.GAME_CELL_H))
            cell_idx_list.append((i,j))
            x_pos += c.GAME_CELL_W
        x_pos = game_area.left
        y_pos += c.GAME_CELL_H

    return cell_rect_list, cell_idx_list



def draw_text_on_rect(screen, font, colour, rect, msg):
    '''
    This function draws text on a rectangle. 

    @params:
        screen - pygame object where everything is being drawn
        font - pygame font being used
        colour - colour of font
        rect - the rectangle where text is drawn on
        msg - The string of text being drawn
    '''
    text = font.render(msg, True, colour)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)


def draw_lines(screen, points_list, colour, x_cells=c.GAME_GRID_W, y_cells=c.GAME_GRID_H):
    '''
    This function draws the connecting lines when point(s) are awarded.

    @params:
        screen - pygame object where everything is being drawn
        points_list - a list of start and end points to draw lines
        colour - colour of line being drawn
        x_cells - number of game columns (needed to scale lines correctly)
        y_cells - number of game columns (needed to scale lines correctly)
    '''
    # Compute total game size area, center it
    x_size = x_cells*c.GAME_CELL_W
    y_size = y_cells*c.GAME_CELL_H
    game_area = pygame.Rect(0, 0, x_size, y_size)
    game_area.center = (c.RESOLUTION_WIDTH / 2, c.RESOLUTION_HEIGHT/2)

    

    for i in range(0, len(points_list)):

        line_start_x = game_area.left + points_list[i][0][1]*c.GAME_CELL_W + c.GAME_CELL_W / 2
        line_start_y = game_area.top +  points_list[i][0][0]*c.GAME_CELL_H + c.GAME_CELL_H / 2
        line_end_x =   game_area.left + points_list[i][2][1]*c.GAME_CELL_W + c.GAME_CELL_W / 2
        line_end_y =   game_area.top +  points_list[i][2][0]*c.GAME_CELL_H + c.GAME_CELL_H / 2

        pygame.draw.line(screen, colour, (line_start_x, line_start_y), (line_end_x, line_end_y), 4)