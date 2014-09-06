#!/usr/bin/env python2.6

'''Game of exploration in a grid-based world'''

import pygame
import time
import TextBox

windowSize = (740, 480)
window = pygame.display.set_mode(windowSize)

from HUD import HUD
from World import World
from WorldView import WorldView

from colours import *
from images import *
import collectables

window.fill(GREY)

pygame.key.set_repeat(100, 75)      # press-and hold for faster movement
USEARROWS = True                    # set the keyboard controls mode

if USEARROWS:                       # mode using arrow keys
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    BLAST = pygame.K_SPACE
else:                               # mode using WASD
    UP = pygame.K_w
    DOWN = pygame.K_s
    LEFT = pygame.K_a
    RIGHT = pygame.K_d
    BLAST = pygame.K_SPACE

def handleevents():
    '''respond to user input'''
    quitting = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitting = True
        if event.type == pygame.KEYDOWN:
            move_x = 0
            move_y = 0
            if event.key == UP:
                move_y -= 1
            if event.key == DOWN:
                move_y += 1
            if event.key == LEFT:
                move_x -= 1
            if event.key == RIGHT:
                move_x += 1
            world.moveplayer(move_x, move_y)
            if event.key == BLAST:
                world.update(world.player.detonate(world.cellmap))
            if world.player.score[collectables.CHOCOLATE] <= 0:
                quitting = True
    return quitting

world = World()
world.moveplayer(0, 0)
worldview = WorldView(world, (0, 0, windowSize[0]-100, windowSize[1]-20), window)
hud = HUD(world, (windowSize[0]-100, 0, 100, windowSize[1]), window)

quitting = False
while not quitting:
    time.sleep(0.04)
    quitting = handleevents()
    scrollpos = worldview.draw(world, window)
    hud.draw(world, window, scrollpos)
    pygame.display.update()

time.sleep(2)
pygame.quit()
