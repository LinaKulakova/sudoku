import pygame
import os
from grid import Grid

# set the window position relative to the screen upper left corner
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400, 100)

# create the window surface and set the window caption
surface = pygame.display.set_mode((1200, 900))
pygame.display.set_caption('Sudoku')

pygame.font.init()
game_font = pygame.font.SysFont('Arial', 50)
game_font2 = pygame.font.SysFont('Arial', 25)

grid = Grid(pygame, game_font)
running = True

# the game loop
while running:

    # check for input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.win:
            if pygame.mouse.get_pressed()[0]:  # check for the left mouse button
                pos = pygame.mouse.get_pos()
                grid.get_mouse_click(pos[0], pos[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.win:
                grid.restart()
            if not grid.win and grid.selected_cell is not None:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    number = event.key - pygame.K_0
                    grid.set_cell_value(grid.selected_cell, number)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    grid.set_cell_value(grid.selected_cell, 0)

    # clear the window surface to black
    surface.fill((0, 0, 0))

    # draw the grid here
    grid.draw_all(pygame, surface)

    if grid.win:
        won_surface = game_font.render("You Won!", False, (0, 255, 0))
        surface.blit(won_surface, (950, 650))

        press_space_surf = game_font2.render("Press Space to restart!", False, (0, 255, 200))
        surface.blit(press_space_surf, (920, 750))

    # update the window surface
    pygame.display.flip()
