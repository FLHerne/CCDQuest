#!/usr/bin/env python2.6

'''Game of exploration in a grid-based world'''

import pygame
import sys
import time
import json

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

currentmap = 0
maps = json.load(open('map/maps.json'))

def loadmap(newmap):
    global hud
    global messagebox
    global world
    global worldview
    global currentmap
    print 'Load world', newmap
    if newmap not in range(len(maps)):
        return False
    currentmap = newmap
    hud.loadingsplash("Loading next level: " + maps[currentmap]['name'])
    pygame.display.update()
    world = World(maps[currentmap])
    messagebox.mgolist = world.bears + world.dragons
    messagebox.string = None
    world.rendervisibletiles()
    window.fill(BLACK)
    hud = HUD(world, window)
    worldview = WorldView(world, window)
    return True

def handleevents():
    '''respond to user input'''
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
        if event.type == pygame.KEYDOWN:
            if event.key == BLAST:
                world.player.detonate(world.cellmap)
            if event.key in MOVEDIRS:
                world.moveplayer(*MOVEDIRS[event.key])
            else:
                world.moveplayer(0, 0)
            if event.key == pygame.K_1:
                loadmap(currentmap - 1)
            if event.key == pygame.K_2:
                loadmap(currentmap + 1)
            if world.player.score[collectables.CHOCOLATE] <= 0:
                gameended = collectables.CHOCOLATE
            if world.player.score[collectables.COIN] == world.cellmap.origcoins:
                if not loadmap(currentmap + 1):
                    gameended = collectables.COIN
            messagebox.update()
    return gameended

world = World(maps[currentmap])
world.moveplayer(0, 0)
HUDWIDTH = 92
worldviewrect = pygame.Rect(0, 0, WINDOWSIZE[0]-HUDWIDTH, WINDOWSIZE[1])
worldview = WorldView(world, window)
hudrect = pygame.Rect(WINDOWSIZE[0]-HUDWIDTH, 0, HUDWIDTH, WINDOWSIZE[1])
hud = HUD(world, window)
messagebox = MessageBox(window, world.bears)
messageboxheight = 25
messageboxpadding = 15
messageboxregion = pygame.Rect(messageboxpadding, WINDOWSIZE[1]-messageboxheight-messageboxpadding, WINDOWSIZE[0]-HUDWIDTH-messageboxpadding, messageboxheight)
gameended = False

while not gameended:
    gameended = handleevents()
    worldviewrect.width = window.get_width()-HUDWIDTH
    worldviewrect.height = window.get_height()
    hudrect.left = window.get_width()-HUDWIDTH
    hudrect.height = window.get_height()
    scrollpos = worldview.draw(worldviewrect, world, window)
    messageboxregion.top = window.get_height()-messageboxheight-messageboxpadding
    messageboxregion.width = window.get_width()-(HUDWIDTH+(2*messageboxpadding))
    messagebox.draw(messageboxregion)
    hud.draw(hudrect, scrollpos)
    if gameended:
        hud.endsplash(gameended)
    pygame.display.update()
    time.sleep(0.05)

time.sleep(2)
pygame.quit()
sys.exit()
