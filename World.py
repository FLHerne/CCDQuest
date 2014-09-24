import pygame
import random
from images import BLOCKSIZE
from Bear import Bear
from Dragon import Dragon
from Map import Map
from Player import Player
from colors import *

class World:
    def __init__(self):
        groundfile = 'map/World7-ground.png'
        collectablefile = 'map/World7-collectables.png'
        self.cellmap = Map(groundfile, collectablefile)
        self.surface = pygame.Surface((self.cellmap.size[0]*BLOCKSIZE, self.cellmap.size[1]*BLOCKSIZE))
        self.surface.fill(BLACK)
        self.player = Player(self.cellmap.startpos)

        def placeBears(number):
            '''randomly add bears to the map'''
            max_attempts = 20 * number
            created = []
            for i in xrange(max_attempts):
                attempt = (random.randint(0, self.cellmap.size[0]-1), random.randint(0, self.cellmap.size[1]-1))
                if self.cellmap[attempt].name not in ['grass', 'forest', 'rocky ground']:
                    continue
                created.append(Bear(attempt))
                if len(created) == number:
                    break
            return created

        self.bears = placeBears(int(self.cellmap.size[0] * self.cellmap.size[1]/2000))

        def placeDragons(number):
            '''randomly add dragons to the map'''
            created = []
            for i in xrange(number):
                pos = (random.randint(0, self.cellmap.size[0]-1), random.randint(0, self.cellmap.size[1]-1))
                created.append(Dragon(pos))
            return created
        self.dragons = placeDragons(int(self.cellmap.size[0] * self.cellmap.size[1]/4000))

    def moveplayer(self, x, y):
        self.player.move(x, y, self.cellmap)
        for x in range(self.player.position[0]-self.player.visibility-1, self.player.position[0]+self.player.visibility+2):
            for y in range(self.player.position[1]-self.player.visibility-1, self.player.position[1]+self.player.visibility+2):
                self.cellmap[x, y].visible = False
        for tile in self.player.visible_tiles(self.cellmap):
            cell = self.cellmap[tile]
            cell.explored = True
            if cell.transparent or list(tile) != self.player.position:
                cell.visible = True
        for x in range(self.player.position[0]-self.player.visibility-2, self.player.position[0]+self.player.visibility+3):
            for y in range(self.player.position[1]-self.player.visibility-2, self.player.position[1]+self.player.visibility+3):
                self.cellmap[x, y].draw(self.surface, x%self.cellmap.size[0], y%self.cellmap.size[1])
        if not self.cellmap[self.player.position].top:
            self.surface.blit(self.player.sprite(), (self.player.position[0]*BLOCKSIZE, self.player.position[1]*BLOCKSIZE))

        for bear in self.bears:
            bear.move(self.player.position, self.cellmap)
            if self.cellmap[bear.position].visible and not  self.cellmap[bear.position].top:
                self.surface.blit(bear.sprite(), (bear.position[0]*BLOCKSIZE, bear.position[1]*BLOCKSIZE))

        for dragon in self.dragons:
            dragon.move(self.player.position, self.cellmap)
            isvisible = False
            for ix in [0, 1]:
                for iy in [0, 1]:
                    if self.cellmap[dragon.position[0]+ix, dragon.position[1]+iy].visible:
                        isvisible = True
            if isvisible:
                offsetsprite = dragon.offsetsprite()
                blitpos = ((dragon.position[0]+offsetsprite[1][0])*BLOCKSIZE,
                           (dragon.position[1]+offsetsprite[1][1])*BLOCKSIZE)
                self.surface.blit(offsetsprite[0], blitpos)
