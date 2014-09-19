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
        self.position = ((self.position[0]+self.direction[0]) % cellmap.size[0],
                         (self.position[1]+self.direction[1]) % cellmap.size[1])

    def sprite(self):
        return images.DragonRedUpLeft
