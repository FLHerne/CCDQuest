import images
import random
from directions import *

class Dragon:
    '''follows you around when in range'''
    def __init__(self, position):
        '''setup bear in given position'''
        self.position = position
        self.direction = UPLEFT

    def move(self, playerpos, cellmap):
        '''fly around the place'''
        def tileoffset(a, b, size):
            subtract = b - a
            absubtract = abs(subtract)
            if absubtract*2 <= size:
                    return subtract
            else:
                    return (size-absubtract) * cmp(0, subtract)

        if not cellmap[playerpos].top:
            offsetx = tileoffset(self.position[0], playerpos[0], cellmap.size[0])
            offsety = tileoffset(self.position[1], playerpos[1], cellmap.size[1])
            newdirection = list(self.direction)
            if abs(offsetx) > abs(offsety):
                newdirection[0] = cmp(offsetx, 0)
            elif abs(offsety) > abs(offsetx):
                newdirection[1] = cmp(offsety, 0)
            self.direction = tuple(newdirection)

        self.position = ((self.position[0]+self.direction[0]) % cellmap.size[0],
                         (self.position[1]+self.direction[1]) % cellmap.size[1])

    def sprite(self):
        return images.DragonRed[self.direction]
