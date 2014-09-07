import pygame
from Cell import *
from colors import *
import collectables


class Map():
    def index(self, coord):
        return (int(coord[0] % self.size[0] * self.size[0]) + coord[1] % self.size[1])

    def __init__(self, groundfile, collectablefile):
        START = MAGENTA
        groundimage = pygame.image.load(groundfile)
        groundmap = pygame.PixelArray(groundimage)
        collectablesimage = pygame.image.load(collectablefile)
        collectablesmap = pygame.PixelArray(collectablesimage)
        self.size = list(groundimage.get_rect().size)
        self.startpos = None
        self.origcoins = 0

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
        print self.origcoins

    def __getitem__(self, coord):
        return self.cellarray[self.index(coord)]

    def __setitem__(self, coord, value):
        self.cellarray[self.index(coord)] = value
