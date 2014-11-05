import pygame
import random
import collectables
import images
from Bear import Bear
from Dragon import Dragon
from Pixie import Pixie
from Sign import Sign
from Map import Map
from Player import Player
from colors import *

TILESIZE = images.TILESIZE

class World:
    def __init__(self, mapdict):
        self.cellmap = Map(mapdict)
        self.surface = pygame.Surface((self.cellmap.size[0]*TILESIZE, self.cellmap.size[1]*TILESIZE))
        self.surface.fill(BLACK)

        self.gemgos = []
        for gemgo in Player, Bear, Dragon, Sign, Pixie:
            self.gemgos += gemgo.place(self.cellmap)
        self.player = filter(lambda x: isinstance(x, Player), self.gemgos)[0]

    def rendervisibletiles(self, extrasprites=[]):
        self.player.updatevisible()
        for tile in self.player.visibletiles:
            cell = self.cellmap[tile]
            cell['explored'] = True
        if not self.cellmap[self.player.position]['transparent']:
            self.player.visibletiles.remove(tuple(self.player.position))
        sprites = extrasprites
        drawntiles = set()
        self.surface.set_clip((self.player.position[0]-self.player.visibility-2)*TILESIZE,
                              (self.player.position[1]-self.player.visibility-2)*TILESIZE,
                              (2*self.player.visibility+4)*TILESIZE,
                              (2*self.player.visibility+4)*TILESIZE)
        for x in range(self.player.position[0]-self.player.visibility-3, self.player.position[0]+self.player.visibility+4):
            for y in range(self.player.position[1]-self.player.visibility-3, self.player.position[1]+self.player.visibility+4):
                modcoord = (x%self.cellmap.size[0],y%self.cellmap.size[1])
                if modcoord not in drawntiles:
                    drawntiles.add(modcoord)
                    sprites += self.cellmap.sprites((x, y))
                    if modcoord not in self.player.visibletiles:
                        sprites.append((images.NonVisible, (x*TILESIZE, y*TILESIZE), 100))
        sprites.sort(key=lambda x: x[2])
        for sprite in sprites:
            for tx in [sprite[1][0]-self.surface.get_width(), sprite[1][0], sprite[1][0]+self.surface.get_width()]:
                for ty in [sprite[1][1]-self.surface.get_height(), sprite[1][1], sprite[1][1]+self.surface.get_height()]:
                    self.surface.blit(sprite[0], (tx, ty))

    def moveplayer(self, arg):
        '''Move the player by (x, y), move other fauna, update world surface around player'''
        self.cellmap.update()
        self.player.action(arg)

        gemgosprites = []
        for gemgo in self.gemgos:
            gemgo.update(self.player)
            sprite = gemgo.sprite(self.player)
            if sprite is not None:
                gemgosprites.append(sprite)

        self.rendervisibletiles(gemgosprites)

        if tuple(self.player.position) in self.cellmap.burningtiles:
            self.player.score[collectables.CHOCOLATE] -= Map.CELLBURNINGCOST
