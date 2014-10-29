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

    def rendervisibletiles(self):
        for x in range(self.player.position[0]-self.player.visibility-1, self.player.position[0]+self.player.visibility+2):
            for y in range(self.player.position[1]-self.player.visibility-1, self.player.position[1]+self.player.visibility+2):
                self.cellmap[x, y]['visible'] = False
        for tile in self.player.visible_tiles():
            cell = self.cellmap[tile]
            cell['explored'] = True
            if cell['transparent'] or list(tile) != self.player.position:
                cell['visible'] = True
        for x in range(self.player.position[0]-self.player.visibility-5, self.player.position[0]+self.player.visibility+6):
            for y in range(self.player.position[1]-self.player.visibility-5, self.player.position[1]+self.player.visibility+6):
                self.cellmap.draw(self.surface, (x%self.cellmap.size[0], y%self.cellmap.size[1]), False)
        for x in range(self.player.position[0]-self.player.visibility-5, self.player.position[0]+self.player.visibility+6):
            for y in range(self.player.position[1]-self.player.visibility-5, self.player.position[1]+self.player.visibility+6):
                self.cellmap.draw(self.surface, (x%self.cellmap.size[0], y%self.cellmap.size[1]), True)
        if not self.cellmap[self.player.position]['top']:
            self.surface.blit(self.player.sprite()[0], (self.player.position[0]*TILESIZE, self.player.position[1]*TILESIZE))

    def moveplayer(self, x, y):
        '''Move the player by (x, y), move other fauna, update world surface around player'''
        self.cellmap.update()
        self.player.move(x, y)

        for dragon in filter(lambda x: isinstance(x, Dragon), self.gemgos):
            dragon.update(self.player.position)

        self.rendervisibletiles()

        for bear in filter(lambda x: isinstance(x, Bear), self.gemgos):
            bear.update(self.player.position)
            if self.cellmap[bear.position]['visible'] and not  self.cellmap[bear.position]['top']:
                self.surface.blit(bear.sprite()[0], (bear.position[0]*TILESIZE, bear.position[1]*TILESIZE))

        for sign in filter(lambda x: isinstance(x, Sign), self.gemgos):
            sign.update(self.player.position)
            if self.cellmap[sign.position]['explored'] and not self.cellmap[sign.position]['top']:
                self.surface.blit(sign.sprite()[0], (sign.position[0]*TILESIZE, sign.position[1]*TILESIZE))

        for dragon in filter(lambda x: isinstance(x, Dragon), self.gemgos):
            isvisible = False
            for ix in [0, 1]:
                for iy in [0, 1]:
                    cell = self.cellmap[dragon.position[0]+ix, dragon.position[1]+iy]
                    if cell['visible'] and not (self.cellmap[self.player.position]['hasroof'] and (cell['hasroof'] or not cell['transparent'])):
                        isvisible = True
            if isvisible:
                offsetsprite = dragon.sprite()
                blitpos = ((dragon.position[0]+offsetsprite[1][0])*TILESIZE,
                           (dragon.position[1]+offsetsprite[1][1])*TILESIZE)
                self.surface.blit(offsetsprite[0], blitpos)

        if tuple(self.player.position) in self.cellmap.burningtiles:
            self.player.score[collectables.CHOCOLATE] -= Map.CELLBURNINGCOST
