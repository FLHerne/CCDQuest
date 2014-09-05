import copy
import pygame
from Cell import *

class Map():
    def index(self, coord):
        return (int(coord[0]%self.size[0]*self.size[0]) + coord[1]%self.size[1])
    
    def __init__(self, groundfile, collectablefile):
        START = MAGENTA
        ground = pygame.image.load(groundfile)
        groundmap = pygame.PixelArray(ground)
        collectables = pygame.image.load(collectablefile)
        collectablesmap = pygame.PixelArray(collectables)
        self.size = list(ground.get_rect().size)
        self.startpos = None
        self.origcoins = 0
        
        self.cellarray = []
        for x in xrange(0, self.size[0]):
            for y in xrange(0, self.size[1]):
                groundcolour = ground.unmap_rgb(groundmap[x, y])
                self.cellarray.append(copy.copy(UnMapGroundColour(groundcolour)))
                collectablecolour = collectables.unmap_rgb(collectablesmap[x, y])
                self.cellarray[self.index((x, y))].collectableItem = UnMapCollectablesColour(collectablecolour)
                if collectablecolour == START:
                    self.startpos = (x, y)
                elif self.cellarray[self.index((x, y))].collectableItem == Cell.COIN:
                    self.origcoins += 1
        print self.origcoins

    def __getitem__(self, coord):
        return self.cellarray[self.index(coord)]
        
    def __setitem__(self, coord, value):
        self.cellarray[self.index(coord)] = value