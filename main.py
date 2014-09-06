#!/usr/bin/env python2.6

'''Game of exploration in a grid-based world'''

import pygame

windowSize = (740, 480)
window = pygame.display.set_mode(windowSize)

import time
import TextBox
from HUD import HUD
from World import World

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

world = World()
world.moveplayer(0, 0)

def HandleEvents():
    '''respond to user input'''
    quitting = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitting = True
        if event.type == pygame.KEYDOWN:
            #if random.random() < 0.7:
                #moveBears(bears)
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

def wrapCoords(scrollpos):
    '''allow world.player to walk around the world in a loop'''
    world.playerx = (world.player.position[0]*BLOCKSIZE)+scrollpos[0]
    world.playery = (world.player.position[1]*BLOCKSIZE)+scrollpos[1]
    if world.player.position[0] % world.cellmap.size[0] == int(world.cellmap.size[0]/2):
        world.player.position[0] %= world.cellmap.size[0]
    if world.player.position[1] % world.cellmap.size[1] == int(world.cellmap.size[1]/2):
        world.player.position[1] %= world.cellmap.size[1]
    return ((-BLOCKSIZE*world.player.position[0])+world.playerx, (-BLOCKSIZE*world.player.position[1])+world.playery)
    
def setup():
    '''to be used at the beginning of the programme'''
    pass

def loop():
    '''to be used repeatedly'''
    pass

def mapWorldToScreen(scrollpos):
    '''show part of the world on screen'''
    old_clip = window.get_clip()
    worldRegion = pygame.Rect(0, 0, windowSize[0]-90, windowSize[1]-20)
    window.set_clip(worldRegion)
    for tx in [scrollpos[0]-world.surface.get_width(), scrollpos[0], scrollpos[0]+world.surface.get_width()]:
        for ty in [scrollpos[1]-world.surface.get_height(), scrollpos[1], scrollpos[1]+world.surface.get_height()]:
            if world.surface.get_rect(topleft=(tx, ty)).colliderect(worldRegion):
                window.blit(world.surface, (tx, ty))
    window.set_clip(old_clip)

def calculateScrollPos(scrollpos):
    '''scroll towards the correct position'''
    world.playerx = (world.player.position[0]*BLOCKSIZE)+scrollpos[0]
    world.playery = (world.player.position[1]*BLOCKSIZE)+scrollpos[1]
    if world.playerx+(world.player.visibility*BLOCKSIZE) > windowSize[0]-100:         #too far right
        scrollStep = (abs((world.playerx+(world.player.visibility*BLOCKSIZE)) - (windowSize[0]-100)) / 2) +1
        scrollpos = (scrollpos[0]-scrollStep, scrollpos[1])
    if world.playerx-(world.player.visibility*BLOCKSIZE) < 0:                         #too far left
        scrollStep = (abs((world.playerx-(world.player.visibility*BLOCKSIZE))) / 2) +1
        scrollpos = (scrollpos[0]+scrollStep, scrollpos[1])
    if world.playery+(world.player.visibility*BLOCKSIZE) > windowSize[1]:             #too far down
        scrollStep = (abs((world.playery+(world.player.visibility*BLOCKSIZE)) - windowSize[1]) / 2) +1
        scrollpos = (scrollpos[0], scrollpos[1]-scrollStep)
    if world.playery-(world.player.visibility*BLOCKSIZE) < 0:                         #too far up
        scrollStep = (abs((world.playery-(world.player.visibility*BLOCKSIZE))) / 2) +1
        scrollpos = (scrollpos[0], scrollpos[1]+scrollStep)

    return scrollpos
    
scrollpos = ((-BLOCKSIZE*world.player.position[0])+((windowSize[0]-100)/2), (-BLOCKSIZE*world.player.position[1])+(windowSize[1]/2))

hud = HUD(world, (windowSize[0]-100, 0, 100, windowSize[1]), window)

quitting = False
while not quitting:
    time.sleep(0.04)
    quitting = HandleEvents()

    scrollpos = calculateScrollPos(scrollpos)
    mapWorldToScreen(scrollpos)
    scrollpos = wrapCoords(scrollpos)
    hud.draw(world, window, scrollpos)

    pygame.display.update()
time.sleep(2)
pygame.quit()
