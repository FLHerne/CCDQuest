import pygame
import random
from Cell import *
from colors import *
import collectables

class Map():
    '''Contains array of Cells and properties representing the map as a whole'''
    def index(self, coord):
        return (int(coord[0] % self.size[0] * self.size[0]) + coord[1] % self.size[1])

    def __init__(self, groundfile, collectablefile):
        '''Load the map from image files'''
        START = MAGENTA
        groundimage = pygame.image.load(groundfile)
        groundmap = pygame.PixelArray(groundimage)
        collectablesimage = pygame.image.load(collectablefile)
        collectablesmap = pygame.PixelArray(collectablesimage)
        self.size = list(groundimage.get_rect().size)
        self.startpos = None
        self.origcoins = 0
        self.burningtiles = set()

        self.cellarray = []
        for x in xrange(0, self.size[0]):
            for y in xrange(0, self.size[1]):
                groundcolour = groundimage.unmap_rgb(groundmap[x, y])
                collectablecolour = collectablesimage.unmap_rgb(collectablesmap[x, y])
                self.cellarray.append(Cell(groundcolour, collectablecolour))
                if collectablecolour == START:
                    self.startpos = (x, y)
                elif self[x, y].collectableitem == collectables.COIN:
                    self.origcoins += 1

    def __getitem__(self, coord):
        '''Get map item with [], wrapping'''
        return self.cellarray[self.index(coord)]

    def __setitem__(self, coord, value):
        '''Set map item with [], wrapping'''
        self.cellarray[self.index(coord)] = value

    def ignite(self, coord):
        '''Attempt to start a fire at coord'''
        cell = self[coord]
        if not cell.flammable:
            return False
        cell.burning = True
        cell.flammable = False
        cell.damaged = True
        self.burningtiles.add((coord[0]%self.size[0], coord[1]%self.size[1]))

    def detonate(self, coord):
        '''Set off an explosion at coord'''
        def blam(epicentre):
            self[epicentre].collectableitem = None
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    cell = self[epicentre[0]+dx, epicentre[1]+dy]
                    if not cell.destroy():
                        continue
                    if cell.collectableitem == collectables.DYNAMITE:
                        blam((epicentre[0]+dx, epicentre[1]+dy))
        if not self[coord].destructable:
            return False
        blam(coord)
        return True

    def update(self):
        '''Spread fire, potentially other continuous map processes'''
        for tile in self.burningtiles.copy():
            cell = self[tile]
            for nbrpos in [(tile[0]-1, tile[1]), (tile[0], tile[1]-1), (tile[0]+1, tile[1]), (tile[0], tile[1]+1)]:
                if random.random() < cell.firespreadchance:
                    self.ignite(nbrpos)
            if random.random() < cell.fireoutchance:
                self[tile].burning = False
                self.burningtiles.remove(tile)
