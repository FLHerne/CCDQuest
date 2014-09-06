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

groundFile = 'map/World7-ground.png'                   # Image to use as map
collectablesFile = 'map/World7-collectables.png'

HUDFONTSIZE = 20                    # Score counter etc

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

cellmap = Map(groundFile, collectablesFile)
world = pygame.Surface((cellmap.size[0]*images.BLOCKSIZE, cellmap.size[1]*images.BLOCKSIZE))
player = Player(cellmap.startpos)

# -----------------------------------------------------------------------------

window.fill(GREY)

# -----------------------------------------------------------------------------


def placeBears(number):
    '''randomly add bears to the map'''
    max_attempts = 20*number
    created = []
    for i in xrange(max_attempts):
        attempt = (random.randint(0,cellmap.size[0]-1), random.randint(0,cellmap.size[1]-1))
        if cellmap[attempt].name not in ['grass', 'forest', 'rocky ground']:
            continue
        created.append(Bear(attempt))
        if len(created) == number:
            break
    return created

def moveBears(bearlist):
    '''make each bear move towards the player using a pathfinder'''
    for bear in bearlist:
        bear.huntplayer(player.position, cellmap)

def drawBears(bearlist, drawSurface):
    '''call the draw function for each bear'''
    for bear in bearlist:
        drawSurface.blit(bear.sprite(), (bear.position[0]*images.BLOCKSIZE, bear.position[1]*images.BLOCKSIZE))

bears = placeBears(int(cellmap.size[0]*cellmap.size[1]/5000))

# -----------------------------------------------------------------------------


def ExplosionValid(x, y, Dynamite):
    '''test if an explosion is currently possible'''
    if (Dynamite <=0):
        DebugPrint("No Dynamite:")
    if not cellmap[x, y].destructable:
        DebugPrint("Current cell cannot be destroyed")
    if (Dynamite > 0 and cellmap[x, y].destructable):
        DebugPrint("Explosion possible")
    else:
        DebugPrint("Explosion not possible")
    return (Dynamite > 0 and cellmap[x, y].destructable)
        
        
def Explosion(Dynamite, Centrex, Centrey):
    '''Clear a 3x3 square using a stick of dynamite'''
    DebugPrint("Explosion at " + str(Centrex) + ", " + str(Centrey))
    for x in (-1, 0, 1):                                                        # explosion forms a 3x3 square
        for y in (-1, 0, 1):
            cellmap[Centrex, Centrey].collectableitem = None
            if cellmap[Centrex+x, Centrey+y].collectableitem == Cell.DYNAMITE:
                Explosion(1, Centrex+x, Centrey+y)                              # dynamite sets off neighbouring dynamite
            if cellmap[Centrex+x, Centrey+y].destructable:
                cellmap[Centrex+x, Centrey+y].solid = False
                cellmap[Centrex+x, Centrey+y].transparent = True
                cellmap[Centrex+x, Centrey+y].damaged = True
                cellmap[Centrex+x, Centrey+y].difficulty += 5
                if not ((x, y) == (0, 0)):
                    cellmap[Centrex+x, Centrey+y].name = "debris from an explosion"
                if cellmap[Centrex+x, Centrey+y].image == images.Wood:
                    cellmap[Centrex+x, Centrey+y].image = images.Water
    Dynamite -= 1
    return Dynamite

def HandleEvents():
    '''respond to user input'''
    quitting = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitting = True
        if event.type == pygame.KEYDOWN:
            if random.random() < 0.7:
                moveBears(bears)
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
            player.move(move_x, move_y, cellmap)
            if event.key == BLAST and ExplosionValid(player.position[0], player.position[1], player.score[collectables.DYNAMITE]):
                player.score[collectables.DYNAMITE] = Explosion(player.score[collectables.DYNAMITE], player.position[0], player.position[1])
            if player.score[collectables.CHOCOLATE] <= 0:
                quitting = True
    return quitting
    
def DrawTiles():
    '''redraw every cell that might be visible or have been visible on the previous draw'''
    for x in range(player.position[0]-player.visibility-1, player.position[0]+player.visibility+2):
        for y in range(player.position[1]-player.visibility-1, player.position[1]+player.visibility+2):
            cellmap[x, y].draw(world, x%cellmap.size[0], y%cellmap.size[1])

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
    '''allow player to walk around the world in a loop'''
    playerx = (player.position[0]*images.BLOCKSIZE)+scrollpos[0]
    playery = (player.position[1]*images.BLOCKSIZE)+scrollpos[1]
    if player.position[0] % cellmap.size[0] == int(cellmap.size[0]/2):
        player.position[0] %= cellmap.size[0]
    if player.position[1] % cellmap.size[1] == int(cellmap.size[1]/2):
        player.position[1] %= cellmap.size[1]
    return ((-images.BLOCKSIZE*player.position[0])+playerx, (-images.BLOCKSIZE*player.position[1])+playery)
    
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
    for tx in [scrollpos[0]-world.get_width(), scrollpos[0], scrollpos[0]+world.get_width()]:
        for ty in [scrollpos[1]-world.get_height(), scrollpos[1], scrollpos[1]+world.get_height()]:
            if world.get_rect(topleft=(tx, ty)).colliderect(worldRegion):
                window.blit(world, (tx, ty))
    window.set_clip(old_clip)

def calculateScrollPos(scrollpos):
    '''scroll towards the correct position'''
    playerx = (player.position[0]*images.BLOCKSIZE)+scrollpos[0]
    playery = (player.position[1]*images.BLOCKSIZE)+scrollpos[1]
    if playerx+(player.visibility*images.BLOCKSIZE) > windowSize[0]-100:         #too far right
        scrollStep = (abs((playerx+(player.visibility*images.BLOCKSIZE)) - (windowSize[0]-100)) / 2) +1
        scrollpos = (scrollpos[0]-scrollStep, scrollpos[1])
        DebugPrint(str(player.position))
        DebugPrint("Scrolled Left" + str(scrollpos))
    if playerx-(player.visibility*images.BLOCKSIZE) < 0:                         #too far left
        scrollStep = (abs((playerx-(player.visibility*images.BLOCKSIZE))) / 2) +1
        scrollpos = (scrollpos[0]+scrollStep, scrollpos[1])
        DebugPrint(str(player.position))
        DebugPrint("Scrolled right" + str(scrollpos))
    if playery+(player.visibility*images.BLOCKSIZE) > windowSize[1]:             #too far down
        scrollStep = (abs((playery+(player.visibility*images.BLOCKSIZE)) - windowSize[1]) / 2) +1
        scrollpos = (scrollpos[0], scrollpos[1]-scrollStep)
        DebugPrint("Scrolled up" + str(scrollpos))
    if playery-(player.visibility*images.BLOCKSIZE) < 0:                         #too far up
        scrollStep = (abs((playery-(player.visibility*images.BLOCKSIZE))) / 2) +1
        scrollpos = (scrollpos[0], scrollpos[1]+scrollStep)
        DebugPrint("Scrolled down" + str(scrollpos))

    return scrollpos
    
scrollpos = ((-images.BLOCKSIZE*player.position[0])+((windowSize[0]-100)/2), (-images.BLOCKSIZE*player.position[1])+(windowSize[1]/2))
DebugPrint("Initial scrollpos" + str(scrollpos))

quitting = False
while not quitting:
    time.sleep(0.04)
    quitting = HandleEvents()
    visible_tiles = player.visible_tiles(cellmap)
    for tile in visible_tiles:
        cellmap[tile].explored = True
        cellmap[tile].visible = True
    DrawTiles()
    drawBears(bears, world)
    playerblit = player.position[0]%cellmap.size[0]*images.BLOCKSIZE, player.position[1]%cellmap.size[0]*images.BLOCKSIZE
    world.blit(player.sprite(), playerblit)
    scrollpos = calculateScrollPos(scrollpos)
    mapWorldToScreen(scrollpos)
    scrollpos = wrapCoords(scrollpos)
    #DrawHud(window)
    
    #newTextBox.Draw(window, "Hello, World!", pygame.Rect((30, 30), (200, 50)))
    
    pygame.display.update()
            
pygame.quit()
sys.exit()