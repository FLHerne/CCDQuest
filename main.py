#!/usr/bin/env python2.6

'''Game of exploration in a grid-based world'''

import pygame
windowSize = (740, 480)
window = pygame.display.set_mode(windowSize)

import sys
import time
import copy
import TextBox
import newTextBox
import random
import images
from Bear import Bear
from Cell import Cell
from HUD import HUD
from Map import Map
from Player import Player
from World import World

from colours import *
import collectables

# -----------------------------------------------------------------------------

printDebug = True
printError = True

def DebugPrint(Message):            # Messages which the end-user need not see, but may be useful to the developer
    if printDebug:
        print(Message)
 
def ErrorPrint(Message):            # Messages which indicate that something has gone wrong
    if printError:
        print("Error: " + Message)

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

window.fill(GREY)

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

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

#Endgame screens
    #if player.score[collectables.CHOCOLATE] <= 0:
        #TextBox.Print(drawSurface,
                      #False,
                      #0, 0,
                      #windowSize[0],
                      #BLACK,
                      #WHITE,
                      #'Arial', HUDFONTSIZE*2,
                      #"You ran out of chocolate!",
                      #True,
                      #[True, windowSize[1]])
    #if player.score[collectables.COIN] >= cellmap.origcoins:
        #TextBox.Print(drawSurface,
                      #False,
                      #0, 0,
                      #windowSize[0],
                      #BLACK,
                      #WHITE,
                      #'Arial', HUDFONTSIZE*2,
                      #"You found all the coins!",
                      #True,
                      #[True, windowSize[1]])

def wrapCoords(scrollpos):
    '''allow world.player to walk around the world in a loop'''
    world.playerx = (world.player.position[0]*images.BLOCKSIZE)+scrollpos[0]
    world.playery = (world.player.position[1]*images.BLOCKSIZE)+scrollpos[1]
    if world.player.position[0] % world.cellmap.size[0] == int(world.cellmap.size[0]/2):
        world.player.position[0] %= world.cellmap.size[0]
    if world.player.position[1] % world.cellmap.size[1] == int(world.cellmap.size[1]/2):
        world.player.position[1] %= world.cellmap.size[1]
    return ((-images.BLOCKSIZE*world.player.position[0])+world.playerx, (-images.BLOCKSIZE*world.player.position[1])+world.playery)
    
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
    world.playerx = (world.player.position[0]*images.BLOCKSIZE)+scrollpos[0]
    world.playery = (world.player.position[1]*images.BLOCKSIZE)+scrollpos[1]
    if world.playerx+(world.player.visibility*images.BLOCKSIZE) > windowSize[0]-100:         #too far right
        scrollStep = (abs((world.playerx+(world.player.visibility*images.BLOCKSIZE)) - (windowSize[0]-100)) / 2) +1
        scrollpos = (scrollpos[0]-scrollStep, scrollpos[1])
        DebugPrint(str(world.player.position))
        DebugPrint("Scrolled Left" + str(scrollpos))
    if world.playerx-(world.player.visibility*images.BLOCKSIZE) < 0:                         #too far left
        scrollStep = (abs((world.playerx-(world.player.visibility*images.BLOCKSIZE))) / 2) +1
        scrollpos = (scrollpos[0]+scrollStep, scrollpos[1])
        DebugPrint(str(world.player.position))
        DebugPrint("Scrolled right" + str(scrollpos))
    if world.playery+(world.player.visibility*images.BLOCKSIZE) > windowSize[1]:             #too far down
        scrollStep = (abs((world.playery+(world.player.visibility*images.BLOCKSIZE)) - windowSize[1]) / 2) +1
        scrollpos = (scrollpos[0], scrollpos[1]-scrollStep)
        DebugPrint("Scrolled up" + str(scrollpos))
    if world.playery-(world.player.visibility*images.BLOCKSIZE) < 0:                         #too far up
        scrollStep = (abs((world.playery-(world.player.visibility*images.BLOCKSIZE))) / 2) +1
        scrollpos = (scrollpos[0], scrollpos[1]+scrollStep)
        DebugPrint("Scrolled down" + str(scrollpos))

    return scrollpos
    
scrollpos = ((-images.BLOCKSIZE*world.player.position[0])+((windowSize[0]-100)/2), (-images.BLOCKSIZE*world.player.position[1])+(windowSize[1]/2))
DebugPrint("Initial scrollpos" + str(scrollpos))

quitting = False
while not quitting:
    time.sleep(0.04)
    quitting = HandleEvents()

    scrollpos = calculateScrollPos(scrollpos)
    mapWorldToScreen(scrollpos)
    scrollpos = wrapCoords(scrollpos)
    #DrawHud(window)
    
    #newTextBox.Draw(window, "Hello, World!", pygame.Rect((30, 30), (200, 50)))
    
    pygame.display.update()
            
pygame.quit()
sys.exit()