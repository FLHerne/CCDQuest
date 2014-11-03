import pygame
import images
from images import TILESIZE
import MGO
import collectables
from colors import *
from directions import *

class Player(MGO.GEMGO):
    '''The player, exploring the grid-based world'''
    FREEPLAYER = False
    XRAYVISION = False

    def __init__(self, position, cellmap):
        '''Initialise instance variables'''
        super(Player, self).__init__(position, cellmap)
        self.color = MAGENTA
        self.visibility = 15
        self.direction = RIGHT
        self.layingfuse = False
        self.score = {
            collectables.COIN: 0,
            collectables.CHOCOLATE: 10000,
            collectables.DYNAMITE: 15
        }

    @classmethod
    def place(cls, cellmap):
        return [cls(cellmap.startpos, cellmap)]

    def update(self, playerpos):
        pass

    def sprite(self):
        return images.Player[self.direction], self._pixelpos(), 0

    def action(self, arg):
        if arg == 'followpath':
            self.followpath()
        elif arg == 'startfuse':
            if not self.layingfuse:
                self.layingfuse = True
                self.score[collectables.DYNAMITE] -= 1
                self.cellmap[self.position]['collectableitem'] = collectables.DYNAMITE
        elif arg == 'ignitefuse':
            self.layingfuse = False
            self.cellmap.ignitefuse(self.position)
        else:
            self.move(*arg)

    def move(self, x, y):
        '''Move if possible, update collectable levels accordingly'''
        if abs(x) + abs(y) != 1:
            return False
        self.direction = (x, y)
        if self.cellmap[self.position[0]+x, self.position[1]+y]['solid'] and not Player.FREEPLAYER:
            self.score[collectables.CHOCOLATE] -= 50
            return False
        self.position = [(self.position[0]+x)%self.cellmap.size[0],
                         (self.position[1]+y)%self.cellmap.size[1]]
        collectable = self.cellmap[self.position]['collectableitem']
        if collectable != 0:
            self.score[collectable] += collectables.value[collectable]
            self._suggestmessage("You pick up " + collectables.name[collectable], 4)
        self.cellmap[self.position]['collectableitem'] = 0
        if not Player.FREEPLAYER:
            self.score[collectables.CHOCOLATE] -= self.cellmap[self.position]['difficulty']
        if self.layingfuse and self.cellmap[self.position]['name'] not in ['water', 'deep water']:
            self.cellmap.placefuse(self.position)
        return True

    def followpath(self):
        def subtuple(a, b):
            return (a[0]-b[0], a[1]-b[1])
        oldpos = subtuple(self.position, self.direction)
        pathnbrs = []
        for nbrpos in [(self.position[0]-1, self.position[1]), (self.position[0], self.position[1]-1), (self.position[0]+1, self.position[1]), (self.position[0], self.position[1]+1)]:
            if (nbrpos == oldpos) or (self.cellmap[nbrpos]['name'] not in ['wooden planking', 'paving']):
                continue
            pathnbrs.append(nbrpos)
        if len(pathnbrs) != 1:
            return False
        self.move(*subtuple(pathnbrs[0], self.position))
        return True

    def detonate(self):
        '''Detonate carried explosives at player's location'''
        if self.score[collectables.DYNAMITE] <= 0:
            return
        if not self.cellmap[self.position]['destructable']:
            return
        self._suggestmessage("You detonate some dynamite", 4)
        self.cellmap.detonate(self.position)
        self.score[collectables.DYNAMITE] -= 1

    def visible_tiles(self):
        '''Calculate and return the set of tiles visible to player'''
        visible = set()

        def square():
            for ix in range(self.position[0]-self.visibility, self.position[0]+self.visibility+1):
                for iy in range(self.position[1]-self.visibility, self.position[1]+self.visibility+1):
                    visible.add((ix, iy))

        def diagonalcheck():
            '''Test visibility along (offset) diagonals away from player'''
            x = self.position[0]
            y = self.position[1]
            visible.add((x, y))                             # make the currently occupied cell visible
            for horizontal in (True, False):                # horizontal and vertical
                for Dir1 in (-1, 1):                        # left/right or up/down
                    for Dir2 in (-1, 1):                    # final division into octants
                        Base = 0                            # how far horizontally or vertically the test ray is from the player
                        while (abs(Base) < self.visibility and
                            self.cellmap[self.position[0]+(Base if horizontal else 0),
                                self.position[1]+(0 if horizontal else Base)]['transparent']):   # repeatedly test if a cell is transparent and within a bounding square
                            #Base += Dir1       # FIXME - either the main diagonals aren't shown, or the ends of the cross aren't
                            if horizontal:
                                x = self.position[0] + Base
                                y = self.position[1]
                            else:
                                x = self.position[0]
                                y = self.position[1] + Base
                            visible.add((x, y))
                            self.cellmap[x, y]['visible'] = True
                            while self.cellmap[x, y]['transparent'] and ((self.position[1]-y)**2) + ((self.position[0]-x)**2) <= self.visibility**2:  # test in bounding circle
                                if horizontal:                                                                      # move diagonally
                                    x += Dir1
                                    y += Dir2
                                else:
                                    x += Dir2
                                    y += Dir1
                                visible.add((x, y))                                                           # make visible
                            visible.add((x, y))                                                               # make the first opaque cell visible too
                            Base += Dir1       # FIXME - either the main diagonals aren't shown, or the ends of the cross aren't
                        visible.add((x, y))

        def crosscheck():
            '''Check visibility straight up, down, left and right'''
            for i in (-1, 1):                                                           # Horizontally left and right
                X = 0                                                                   # start at the player
                while self.cellmap[(X*i)+self.position[0], self.position[1]]['transparent'] and X < self.visibility:     # if transparent and within bounding range
                    visible.add(((X*i)+self.position[0], self.position[1]))
                    X += 1                                                              # move away from player
                visible.add(((X*i)+self.position[0], self.position[1]))                 # make final cell visible
            for i in (-1, 1):                                                           # Repeat as above, but vertically
                Y = 0
                while self.cellmap[self.position[0], (Y*i)+self.position[1]]['transparent'] and Y < self.visibility:
                    visible.add((self.position[0], (Y*i)+self.position[1]))
                    Y += 1
                visible.add((self.position[0], (Y*i)+self.position[1]))

        if Player.XRAYVISION:
            square()
        else:
            diagonalcheck()
            crosscheck()
        return visible
