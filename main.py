'''
Main script for the SOS-python game, the classic grid-paper game. 

@author: Hayden Banting
@version: 16 May 2020
'''

## Imports
import pygame
import numpy as np
from config import constants as c
from utility import drawing_functions as df
from utility import grid_functions as gf
from ai import ai_functions as aif

## Set-up
pygame.init()
screen = pygame.display.set_mode((c.RESOLUTION_WIDTH,c.RESOLUTION_HEIGHT))
screen.fill(pygame.Color('white'))
pygame.display.set_caption(c.GAME_TITLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 25)

## Create the play button (w/ hitbox)
play_button_rect = pygame.Rect(c.PLAY_BUTTON_X, c.PLAY_BUTTON_Y, c.PLAY_BUTTON_W, c.PLAY_BUTTON_H)
play_button = pygame.draw.rect(screen, c.PLAY_BUTTON_COLOUR, (c.PLAY_BUTTON_X, c.PLAY_BUTTON_Y, c.PLAY_BUTTON_W, c.PLAY_BUTTON_H))
df.draw_text_on_rect(screen, font, c.PLAY_BUTTON_TEXT_COLOUR, play_button, c.PLAY_BUTTON_TEXT)

## create score boxes
player_score_box = pygame.draw.rect(screen, c.PLAYER_SCORE_BOX_COLOUR, (c.PLAYER_SCORE_BOX_X, c.PLAYER_SCORE_BOX_Y, c.PLAYER_SCORE_BOX_W, c.PLAYER_SCORE_BOX_H))
ai_score_box = pygame.draw.rect(screen, c.AI_SCORE_BOX_COLOUR, (c.AI_SCORE_BOX_X, c.AI_SCORE_BOX_Y, c.AI_SCORE_BOX_W, c.AI_SCORE_BOX_H))

## Main menu loop
on_start_screen = True
while on_start_screen:

    for event in pygame.event.get():
        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP:
            # if the left button is pressed
            if event.button == 1 or event.button == 3:
                pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(pos):
                    screen.fill(pygame.Color('white'))
                    on_start_screen = False

        if event.type == pygame.QUIT:
            on_start_screen = False
            pygame.quit()
            quit()

    pygame.display.update()
    clock.tick(c.GAME_FPS)

## Set-up for main game

game_array = gf.create_game_array()                  # game array (keeps track of all cells, either 'S', 'O', or unfilled)
cell_rect_list, cell_idx_list = df.draw_grid(screen) # hit boxes and correspoing game array indexes of each cell

points_list = []    # keeps track of all sos' on the grid 
player_points = 0   # number of player points
ai_points = 0       # number of ai points


## Main game loop
on_game_screen = True
player_turn = True
ai_turn = False
while on_game_screen:

    # Every loop to-do
    pygame.draw.rect(screen, c.PLAYER_SCORE_BOX_COLOUR, (c.PLAYER_SCORE_BOX_X, c.PLAYER_SCORE_BOX_Y, c.PLAYER_SCORE_BOX_W, c.PLAYER_SCORE_BOX_H))
    df.draw_text_on_rect(screen, font, c.PLAYER_COLOUR, player_score_box, c.PLAYER_SCORE_BOX_TEXT+str(player_points))
    pygame.draw.rect(screen, c.AI_SCORE_BOX_COLOUR, (c.AI_SCORE_BOX_X, c.AI_SCORE_BOX_Y, c.AI_SCORE_BOX_W, c.AI_SCORE_BOX_H))
    df.draw_text_on_rect(screen, font, c.AI_COLOUR, ai_score_box, c.AI_SCORE_BOX_TEXT+str(ai_points))
    pygame.display.update()
    clock.tick(c.GAME_FPS)

    # PLAYER TURN

    if player_turn:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                on_game_screen = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONUP:

                # check if a cell was clicked
                pos = pygame.mouse.get_pos()
                idx = gf.check_for_grid_click(pos, cell_rect_list)

                # if a cell was checked, process
                if idx > -1:
                    if event.button == 1: # left click
                        df.draw_text_on_rect(screen, font, (0,0,0), cell_rect_list[idx], 'S')
                        game_array[cell_idx_list[idx]] = 'S'
                    if event.button == 3: # right click
                        df.draw_text_on_rect(screen, font, (0,0,0), cell_rect_list[idx], 'O')
                        game_array[cell_idx_list[idx]] = 'O'

                    # remove this cell remove the list, can no longer be clicked
                    cell_rect_list.pop(idx)
                    cell_idx_list.pop(idx)

                    # check for an sos
                    new_points, new_points_list = gf.check_for_sos(game_array, points_list)

                    # update points
                    player_points += new_points

                    # draw player lines
                    df.draw_lines(screen, new_points_list, c.PLAYER_COLOUR)

                    # update list of all points (player and ai)
                    points_list = points_list + new_points_list

                    # end of player turn
                    if (new_points == 0):
                        player_turn = False
                        ai_turn = True

                    # Check for game over
                    if len(cell_idx_list) < 1:
                        ai_turn = False
                        player_turn = True
                        print('Game over!')

                    # Refresh screen
                    pygame.display.update()

    # AI TURN

    if ai_turn:

        # Try to make a good move (get points)
        idx, move = aif.check_for_good_move(cell_idx_list, game_array, points_list)

        if idx < 0: # no moves will get points

            # Try to make a safe move (random)
            idx, move = aif.random_safe_move(cell_idx_list, game_array, points_list)

            if idx < 0: # no safe moves left (player could score next turn)

                # play completely randomly
                #idx = aif.select_random_cell(cell_idx_list)
                #move = aif.select_random_char()
                print('random ai move')
                idx, move = aif.random_move(cell_idx_list)

        df.draw_text_on_rect(screen, font, (0,0,0), cell_rect_list[idx], move)
        game_array[cell_idx_list[idx]] = move

        # remove this cell remove the list, can no longer be clicked
        cell_rect_list.pop(idx)
        cell_idx_list.pop(idx)

        # check for an sos
        new_points, new_points_list = gf.check_for_sos(game_array, points_list)

        # update points
        ai_points += new_points

        # draw player lines
        df.draw_lines(screen, new_points_list, c.AI_COLOUR)

        # update list of all points (player and ai)
        points_list = points_list + new_points_list
        
        # end of turn
        if (new_points == 0):
            ai_turn = False
            player_turn = True

        # Check for game over
        if len(cell_idx_list) < 1:
            ai_turn = False
            player_turn = True
            print('Game over!')

        # Refresh screen
        pygame.display.update()

    
