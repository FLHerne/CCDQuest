import images
import random

class Dragon:
    '''follows you around when in range'''

    UPLEFT = (-1,-1)
    UPRIGHT = (1,-1)
    DOWNLEFT = (-1,1)
    DOWNRIGHT = (1,1)

    def __init__(self, position):
        '''setup bear in given position'''
        self.position = position
        self.direction = Dragon.UPLEFT
        self.speed = 0.9

    def move(self, playerpos, cellmap):
        '''fly around the place'''
        def tileoffset(a, b, size):
            subtract = b - a
            absubtract = abs(subtract)
            if absubtract*2 <= size:
                    return subtract
            else:
                    return (size-absubtract) * cmp(0, subtract)

        newdirection = [0, 0]
        offsetx = tileoffset(self.position[0], playerpos[0], cellmap.size[0])
        offsety = tileoffset(self.position[1], playerpos[1], cellmap.size[1])
        if abs(offsety) > abs(offsetx):
            newdirection[0] = self.direction[0]
            newdirection[1] = cmp(offsety, 0)
        else:
            newdirection[0] = cmp(offsetx, 0)
            newdirection[1] = self.direction[1]
        self.direction = tuple(newdirection)

        self.position = ((self.position[0]+self.direction[0]) % cellmap.size[0],
                         (self.position[1]+self.direction[1]) % cellmap.size[1])

    def sprite(self):
        return images.DragonRedUpLeft
