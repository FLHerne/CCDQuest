#!/usr/bin/env python2.6

'''Game of exploration in a grid-based world'''

import pygame
import time

WINDOWSIZE = (740, 480)
window = pygame.display.set_mode(WINDOWSIZE)

from HUD import HUD
from World import World
from WorldView import WorldView

from KeySettings import *
import collectables


def handleevents():
    '''respond to user input'''
    quittrigger = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
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
                quittrigger = True
    return quittrigger

world = World()
world.moveplayer(0, 0)
worldviewrect = (0, 0, WINDOWSIZE[0] - 90, WINDOWSIZE[1] - 20)
worldview = WorldView(world, worldviewrect, window)
hud = HUD(world, (WINDOWSIZE[0] - 100, 0, 100, WINDOWSIZE[1]), window)

quitting = False
while not quitting:
    time.sleep(0.04)
    quitting = handleevents()
    scrollpos = worldview.draw(world, window)
    hud.draw(world, window, scrollpos)
    pygame.display.update()

time.sleep(2)
pygame.quit()
