import random
from directions import *
import images
import MGO

class Dragon(MGO.GEMGO):
    '''Harmless flying thing that follows the player'''
    PER_TILE = 1/float(6000)
    detectionrange = 18
    speed = 0.8

    def __init__(self, position, cellmap):
        '''Create new dragon in position'''
        super(Dragon, self).__init__(position, cellmap)
        self.direction = UPLEFT
        self.hunting = False

    def update(self, player):
        '''Fly toward the player if nearby, or continue in same direction'''
        playerpos = player.position
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

        def flameplayer():
            def addtuple(a, b, c=1):
                return (a[0]+b[0]*c, a[1]+b[1]*c)
            fronttiles = [addtuple(self.position, self.direction, i) for i in range(1,4)]
            for tile in fronttiles:
                if tile == tuple(playerpos):
                    self._suggestmessage("The dragon breaths a jet of fire towards you", 5)
                    for tile in fronttiles:
                        self.cellmap.ignite(tile, forceignite=True)
                    break

        washunting = self.hunting
        if not self.cellmap[playerpos]['top'] and not self.cellmap[playerpos]['hasroof'] and random.random() < Dragon.speed:
            offset = tileoffset(self.position, playerpos, self.cellmap.size)
            if offset[0]**2 + offset[1]**2 <= Dragon.detectionrange**2:
                self.hunting = True
                newdirection = list(self.direction)
                if abs(offset[0]) > abs(offset[1]):
                    newdirection[0] = cmp(offset[0], 0)
                elif abs(offset[1]) > abs(offset[0]):
                    newdirection[1] = cmp(offset[1], 0)
                elif cmp(offset[0], 0) != cmp(newdirection[0], 0):
                    newdirection[0] = -self.direction[0]
                elif cmp(offset[1], 0) != cmp(newdirection[1], 0):
                    newdirection[1] = -self.direction[1]
                self.direction = tuple(newdirection)
        else:
            self.hunting = False
        if self.hunting:
            if washunting:
                self._suggestmessage("You are being hunted down by a dragon", 2)
            else:
                self._suggestmessage("A dragon begins to chase you", 3)
        else:
            if washunting:
                self._suggestmessage("The dragon starts to fly away", 1)

        self.position = ((self.position[0]+self.direction[0]) % self.cellmap.size[0],
                         (self.position[1]+self.direction[1]) % self.cellmap.size[1])
        flameplayer()

    def sprite(self, player):
        isvisible = False
        for ix, iy in [(0,0), (0,1), (1,0), (1,1)]:
            if (self.position[0]+ix, self.position[1]+iy) in player.visibletiles:
                isvisible = True
                break
        if isvisible:
            offset = [-images.TILESIZE if axis == 1 else 0 for axis in self.direction]
            return (images.DragonRed[self.direction],
                    self._pixelpos(offset),
                    20)
        else:
            return None
