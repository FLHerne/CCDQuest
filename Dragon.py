import random
from directions import *
import images

class Dragon:
    '''Harmless flying thing that follows the player'''
    detectionrange = 18
    speed = 0.8

    def __init__(self, position):
        '''Create new dragon in position'''
        self.position = position
        self.direction = UPLEFT

    def move(self, playerpos, cellmap):
        '''Fly toward the player if nearby, or continue in same direction'''
        def tileoffset(a, b, size):
            offset = [0, 0]
            for axis in [0, 1]:
                subtract = b[axis] - a[axis]
                absubtract = abs(subtract)
                if absubtract*2 <= size:
                    offset[axis] = subtract
                else:
                    offset[axis] = (size-absubtract) * cmp(0, subtract)
            return offset

        if not cellmap[playerpos].top and random.random() < Dragon.speed:
            offset = tileoffset(self.position, playerpos, cellmap.size)
            if offset[0]**2 + offset[1]**1 <= Dragon.detectionrange**2:
                newdirection = list(self.direction)
                if abs(offset[0]) > abs(offset[1]):
                    newdirection[0] = cmp(offset[0], 0)
                elif abs(offset[1]) > abs(offset[0]):
                    newdirection[1] = cmp(offset[1], 0)
                self.direction = tuple(newdirection)

        self.position = ((self.position[0]+self.direction[0]) % cellmap.size[0],
                         (self.position[1]+self.direction[1]) % cellmap.size[1])

    def offsetsprite(self):
        '''Returns sprite plus offset in tiles'''
        return images.DragonRed[self.direction], [-1 if axis == 1 else 0 for axis in self.direction]
