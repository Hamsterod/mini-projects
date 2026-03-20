import random

import pygame
import gameloop
import ai
from pygame import Vector2

import cell

pygame.init()
screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption("TicTacToe", "TicTacToe")
clock = pygame.time.Clock()
running = True

colours = ["#f5e9d0", "#73a7f5", "#f58973"]

cell1 = cell.Cell(Vector2(0, 0), 0)
cell2 = cell.Cell(Vector2(1, 0), 0)
cell3 = cell.Cell(Vector2(2, 0), 0)
cell4 = cell.Cell(Vector2(0, 1), 0)
cell5 = cell.Cell(Vector2(1, 1), 0)
cell6 = cell.Cell(Vector2(2, 1), 0)
cell7 = cell.Cell(Vector2(0, 2), 0)
cell8 = cell.Cell(Vector2(1, 2), 0)
cell9 = cell.Cell(Vector2(2, 2), 0)

cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

vic_team = gameloop.check_victory(cells)

last_restart = 0
restarting = False

def update():
    global restarting, last_restart, vic_team

    if vic_team[2] != 0 or restarting is True:
        if restarting is False:
            last_restart = pygame.time.get_ticks()
            restarting = True
        if pygame.time.get_ticks() > last_restart + 300:
            for x in cells:
                x.cell_type = 0
            last_restart = pygame.time.get_ticks()
            restarting = False
            cells[random.randrange(9)].cell_type = 1
            gameloop.team1 = False
            ai.last_update = pygame.time.get_ticks()

            if vic_team[2] == 2:
                ai.reward()
                ai.slap2()
            elif vic_team[2] == 1:
                ai.slap()
                ai.reward2()
    a = 0
    if restarting is False:
        for h in cells:
            if h.cell_type != 0:
                a += 1
            if a == 9:
                last_restart = pygame.time.get_ticks()
                restarting = True

    vic_team = gameloop.check_victory(cells)
    ai.move(cells, restarting, pygame.time.get_ticks())


def render():
    global vic_team

    screen.fill("#f5e9d0")

    for c in cells:
        c.draw_cell(screen)

    pygame.draw.line(screen, colours[vic_team[2]], [vic_team[0][0] * screen.get_width() / 3 + screen.get_width() / 6, vic_team[0][1] * screen.get_height() / 3 + screen.get_width() / 6], [vic_team[1][0] * screen.get_width() / 3 + screen.get_width() / 6, vic_team[1][1] * screen.get_height() / 3 + screen.get_width() / 6], 15)

    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if event.type == pygame.MOUSEBUTTONDOWN:
        #    gameloop.check_input(event.dict, cells, screen)

    update()
    render()

pygame.quit()