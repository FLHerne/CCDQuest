#!/usr/bin/env python2.6

'''Game of exploration in a grid-based world'''

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

from keysettings import *
import collectables
import images

def handleevents():
    '''respond to user input'''
    gameended = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.VIDEORESIZE:
            size = event.dict['size']
            if size[1] >= 180:
                window = pygame.display.set_mode(size, pygame.RESIZABLE)
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
                world.player.detonate(world.cellmap)
                world.moveplayer(0, 0)
            if world.player.score[collectables.CHOCOLATE] <= 0:
                gameended = collectables.CHOCOLATE
            if world.player.score[collectables.COIN] == world.cellmap.origcoins:
                gameended = collectables.COIN
    return gameended

world = World()
world.moveplayer(0, 0)
HUDWIDTH = 92
worldviewrect = pygame.Rect(0, 0, WINDOWSIZE[0]-HUDWIDTH, WINDOWSIZE[1])
worldview = WorldView(world, window)
hudrect = pygame.Rect(WINDOWSIZE[0]-HUDWIDTH, 0, HUDWIDTH, WINDOWSIZE[1])
hud = HUD(world, window)
messagebox = MessageBox(world, window)
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
    messageboxregion.width = window.get_width()-(HUDWIDTH+(2*messageboxpadding))
    string = "Hello, world"
    messagebox.draw(messageboxregion, string)
    hud.draw(hudrect, scrollpos)
    if gameended:
        hud.endsplash(gameended)
    pygame.display.update()
    time.sleep(0.04)

time.sleep(2)
pygame.quit()
sys.exit()
