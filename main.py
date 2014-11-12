#!/usr/bin/env python2.6

"""Game of exploration in a grid-based world"""

import pygame
import sys
import time

pygame.init()
WINDOWSIZE = (800, 480)
window = pygame.display.set_mode(WINDOWSIZE, pygame.RESIZABLE)

from HUD import HUD
from MessageBox import MessageBox
from World import World
from WorldView import WorldView

from colors import *

from keysettings import *
import collectables

import gamestate

def loadmap(name):
    if name is None:
        return False
    global hud
    global messagebox
    global world
    global worldview
    global currentmap

    hud.loadingsplash("Loading next level: " + name)
    pygame.display.update()
    gamestate.loadworld(name)
    world = gamestate.currentworld

    messagebox = MessageBox(window, world.gemgos)

    messagebox.string = None
    world.moveplayer((0, 0))
    window.fill(BLACK)
    hud = HUD(world, window)
    worldview = WorldView(world, window)
    return True

def handleevents():
    """respond to user input"""
    global world
    global currentmap
    global window
    gameended = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.VIDEORESIZE:
            size = event.dict['size']
            if size[0] >= 320 and size[1] >= 240:
                window = pygame.display.set_mode(size, pygame.RESIZABLE)
        if event.type == pygame.KEYUP:
            if event.key == FUSEREEL:
                world.moveplayer('ignitefuse')
        if event.type == pygame.KEYDOWN:
            if event.key in MOVEDIRS:
                world.moveplayer(MOVEDIRS[event.key])
            elif event.key == FOLLOWPATH:
                world.moveplayer('followpath')
            elif event.key == FUSEREEL:
                world.moveplayer('startfuse')
            elif event.key == pygame.K_3:
                world.moveplayer('scattercoins')
            else:
                world.moveplayer((0, 0))
            if event.key == pygame.K_1:
                loadmap(gamestate.stepname(-1))
            if event.key == pygame.K_2:
                loadmap(gamestate.stepname(1))
            if world.player.score[collectables.CHOCOLATE] <= 0:
                gameended = collectables.CHOCOLATE
            if world.player.score[collectables.COIN] == world.cellmap.origcoins:
                nextmap = gamestate.stepname(1)
                if nextmap is None:
                    gameended = collectables.COIN
            messagebox.update()
    return gameended

world = gamestate.currentworld
world.moveplayer((0, 0))
HUDWIDTH = 92
worldviewrect = pygame.Rect(0, 0, WINDOWSIZE[0]-HUDWIDTH, WINDOWSIZE[1])
worldview = WorldView(world, window)
hudrect = pygame.Rect(WINDOWSIZE[0]-HUDWIDTH, 0, HUDWIDTH, WINDOWSIZE[1])
hud = HUD(world, window)

messagebox = MessageBox(window, world.gemgos)

messageboxheight = 25
messageboxpadding = 15
messageboxregion = pygame.Rect(messageboxpadding, WINDOWSIZE[1]-messageboxheight-messageboxpadding, WINDOWSIZE[0]-HUDWIDTH-messageboxpadding, messageboxheight)
gameended = False

while not gameended:
    loopstarttime = time.clock()
    gameended = handleevents()
    worldviewrect.width = window.get_width()-HUDWIDTH
    worldviewrect.height = window.get_height()
    hudrect.left = window.get_width()-HUDWIDTH
    hudrect.height = window.get_height()
    scrollpos = worldview.draw(worldviewrect)
    messageboxregion.top = window.get_height()-messageboxheight-messageboxpadding
    messageboxregion.width = window.get_width()-(HUDWIDTH+(2*messageboxpadding))
    messagebox.draw(messageboxregion)
    hud.draw(hudrect, scrollpos)
    if gameended:
        hud.endsplash(gameended)
    pygame.display.update()
    time.sleep(max(0.05 + loopstarttime - time.clock(), 0))

time.sleep(2)
pygame.quit()
sys.exit()
