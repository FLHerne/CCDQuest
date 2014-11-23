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

from Player import Player
player1 = Player()

def handleevents(player):
    """respond to user input"""
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
                player.action('ignitefuse')
        if event.type == pygame.KEYDOWN:
            if player.state in ['lost', 'won', 'crashed']:
                time.sleep(2)
                sys.exit()
            if event.key in MOVEDIRS:
                player.action(MOVEDIRS[event.key])
            elif event.key == FOLLOWPATH:
                player.action('followpath')
            elif event.key == FUSEREEL:
                player.action('startfuse')
            elif event.key == pygame.K_3:
                player.action('scattercoins')
            else:
                player.action((0, 0))
            if event.key == pygame.K_1:
                player.stepworld(-1)
            if event.key == pygame.K_2:
                player.stepworld(1)
            messagebox.update()

HUDWIDTH = 92
MBOXHEIGHT = 25
MBOXPADDING = 15

worldview = WorldView(player1, window)
messagebox = MessageBox(player1, window)
hud = HUD(player1, window)

while True:
    loopstarttime = time.clock()
    handleevents(player1)
    hudborderx = window.get_width()-HUDWIDTH
    worldviewregion = pygame.Rect(0, 0, hudborderx, window.get_height())
    hudregion = pygame.Rect(hudborderx, 0, HUDWIDTH, window.get_height())
    messageboxregion = pygame.Rect(0, window.get_height()-MBOXHEIGHT-MBOXPADDING,
                                  hudborderx - 2*MBOXPADDING,
                                  MBOXHEIGHT + 2*MBOXPADDING)
    scrollpos = worldview.draw(worldviewregion)
    messagebox.draw(messageboxregion)
    hud.draw(hudregion, scrollpos)
    pygame.display.update()
    time.sleep(max(0.05 + loopstarttime - time.clock(), 0))
