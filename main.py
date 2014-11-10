#!/usr/bin/env python2.6

"""Game of exploration in a grid-based world"""

import pygame
import sys
import time
import os
import json
import ConfigParser

pygame.init()
WINDOWSIZE = (800, 480)
window = pygame.display.set_mode(WINDOWSIZE, pygame.RESIZABLE)

from HUD import HUD
from MessageBox import MessageBox
from Bear import Bear
from Dragon import Dragon
from Player import Player
from World import World
from WorldView import WorldView

from colors import *

from keysettings import *
import collectables

currentmap = 0
maps = []

mainconfig = ConfigParser.RawConfigParser()
loaded = mainconfig.read("CCDQuest.cfg")
if not loaded or not mainconfig.has_section("maps"):
    print "Config error!"
    sys.exit(1)
if mainconfig.has_section("settings"):
    if mainconfig.has_option("settings", "freeplayer"):
        try:
            Player.FREEPLAYER = mainconfig.getboolean("settings", "freeplayer")
        except ValueError:
            print "Invalid value for 'freeplayer'"
    if mainconfig.has_option("settings", "xrayvision"):
        try:
            Player.XRAYVISION = mainconfig.getboolean("settings", "xrayvision")
        except ValueError:
            print "Invalid value for 'xrayvision'"
if mainconfig.has_section("fauna"):
    if mainconfig.has_option("fauna", "tiles_per_bear"):
        try:
            Bear.PER_TILE = 1/mainconfig.getfloat("fauna", "tiles_per_bear")
        except ValueError:
            print "Invalid value for 'tiles_per_bear'"
    if mainconfig.has_option("fauna", "tiles_per_dragon"):
        try:
            Dragon.PER_TILE = 1/mainconfig.getfloat("fauna", "tiles_per_dragon")
        except ValueError:
            print "Invalid value for 'tiles_per_dragon'"
for im in mainconfig.items("maps"):
    descfilename = os.path.join('map', im[1], 'mapdesc.json')
    try:
        imfile = open(descfilename)
    except:
        print "Unable to load map", im[0]+":"
        print "File", descfilename, "unreadable or missing"
        continue
    try:
        newmap = json.load(imfile)
    except ValueError as err:
        print "Unable to load map", im[0]+":"
        print err
        continue
    imfile.close()
    newmap['dir'] = im[1]
    maps.append(newmap)
if not len(maps):
    print "No loadable maps!"
    sys.exit(1)

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

    messagebox.mgolist = world.gemgos

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
    scrollpos = worldview.draw(worldviewrect, world, window)
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
