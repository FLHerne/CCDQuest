#!/usr/bin/env python2.6

"""Game of exploration in a grid-based world"""

import pygame
import sys
import time
import coords

pygame.init()
WINDOWSIZE = (800, 480)
window = pygame.display.set_mode(WINDOWSIZE, pygame.RESIZABLE)

from HUD import HUD
from MessageBox import MessageBox
from WorldView import WorldView

from colors import *

from keysettings import *
import collectables

import gamestate

def handleevents():
    """respond to user input"""
    world = gamestate.getstate(0, 'world')
    global window
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
            if gamestate.getstate(0, 'state') in ['lost', 'won']:
                time.sleep(2)
                sys.exit()
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
                gamestate.stepworld(-1)
            if event.key == pygame.K_2:
                gamestate.stepworld(1)
            messagebox.update()

HUDWIDTH = 92
MBOXHEIGHT = 25
MBOXPADDING = 15

worldview = WorldView(window)
messagebox = MessageBox(window)
hud = HUD(window)

while True:
    loopstarttime = time.clock()
    gameended = handleevents()
    hudborderx = window.get_width()-HUDWIDTH
    worldviewregion = pygame.Rect(0, 0, hudborderx, window.get_height())
    hudregion = pygame.Rect(hudborderx, 0, HUDWIDTH, window.get_height())
    messageboxregion = pygame.Rect(0, window.get_height()-MBOXHEIGHT-MBOXPADDING,
                                  hudborderx-(2*MBOXPADDING),
                                  window.get_height()-MBOXHEIGHT-MBOXPADDING)
    scrollpos = worldview.draw(worldviewregion)
    messagebox.draw(messageboxregion)
    hud.draw(hudregion, scrollpos)
    pygame.display.update()
    time.sleep(max(0.05 + loopstarttime - time.clock(), 0))
