import pygame
import random
import collectables
from images import TILESIZE
from Bear import Bear
from Dragon import Dragon
from Sign import Sign
from Map import Map
from Player import Player
from colors import *

class World:
    def __init__(self, mapdict):
        self.cellmap = Map(mapdict)
        self.surface = pygame.Surface((self.cellmap.size[0]*TILESIZE, self.cellmap.size[1]*TILESIZE))
        self.surface.fill(BLACK)

        self.gemgos = []
        for gemgo in Player, Bear, Dragon, Sign:
            self.gemgos += gemgo.place(self.cellmap)
        self.player = filter(lambda x: isinstance(x, Player), self.gemgos)[0]

    def rendervisibletiles(self, extrasprites=[]):
        for x in range(self.player.position[0]-self.player.visibility-1, self.player.position[0]+self.player.visibility+2):
            for y in range(self.player.position[1]-self.player.visibility-1, self.player.position[1]+self.player.visibility+2):
                self.cellmap[x, y]['visible'] = False
        for tile in self.player.visible_tiles():
            cell = self.cellmap[tile]
            cell['explored'] = True
            if cell['transparent'] or list(tile) != self.player.position:
                cell['visible'] = True
        sprites = extrasprites
        for x in range(self.player.position[0]-self.player.visibility-5, self.player.position[0]+self.player.visibility+6):
            for y in range(self.player.position[1]-self.player.visibility-5, self.player.position[1]+self.player.visibility+6):
                sprites += self.cellmap.sprites((x%self.cellmap.size[0], y%self.cellmap.size[1]))
        sprites.sort(key=lambda x: x[2])
        for sprite in sprites:
            self.surface.blit(sprite[0], sprite[1])

    def moveplayer(self, x, y):
        '''Move the player by (x, y), move other fauna, update world surface around player'''
        self.cellmap.update()
        self.player.move(x, y)

        gemgosprites = []
        for gemgo in self.gemgos:
            gemgo.update(self.player.position)
            sprite = gemgo.sprite()
            if sprite is not None:
                gemgosprites.append(sprite)

        self.rendervisibletiles(gemgosprites)

        if tuple(self.player.position) in self.cellmap.burningtiles:
            self.player.score[collectables.CHOCOLATE] -= Map.CELLBURNINGCOST
