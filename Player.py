import pygame
import images
from images import TILESIZE
import collectables
from colors import *
from directions import *

# Remove solidity and movement cost for testing
FREEPLAYER = False

class Player:
    '''The player, exploring the grid-based world'''
    def __init__(self, position):
        '''Initialise instance variables'''
        self.animcounter = 0
        self.color = MAGENTA
        self.visibility = 15
        self.position = list(position)
        self.direction = RIGHT
        self.score = {
            collectables.COIN: 0,
            collectables.CHOCOLATE: 10000,
            collectables.DYNAMITE: 15
        }

    def move(self, x, y, cellmap):
        '''Move if possible, update collectable levels accordingly'''
        if abs(x) + abs(y) != 1:
            return False
        self.direction = (x, y)
        if cellmap[self.position[0]+x, self.position[1]+y].solid and not FREEPLAYER:
            self.score[collectables.CHOCOLATE] -= 50
            return False
        self.position = [(self.position[0]+x)%cellmap.size[0],
                         (self.position[1]+y)%cellmap.size[1]]
        collectable = cellmap[self.position].collectableitem
        if collectable != None:
            self.score[collectable] += collectables.value[collectable]
        cellmap[self.position].collectableitem = None
        if not FREEPLAYER:
            self.score[collectables.CHOCOLATE] -= cellmap[self.position].difficulty
        return True

    def sprite(self):
        return images.Player[self.direction]

    def visible_tiles(self, cellmap):
        '''Calculate and return the set of tiles visible to player'''
        visible = set()

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
                            cellmap[self.position[0]+(Base if horizontal else 0),
                                self.position[1]+(0 if horizontal else Base)].transparent):   # repeatedly test if a cell is transparent and within a bounding square
                            #Base += Dir1       # FIXME - either the main diagonals aren't shown, or the ends of the cross aren't
                            if horizontal:
                                x = self.position[0] + Base
                                y = self.position[1]
                            else:
                                x = self.position[0]
                                y = self.position[1] + Base
                            visible.add((x, y))
                            cellmap[x, y].visible = True
                            while cellmap[x, y].transparent and ((self.position[1]-y)**2) + ((self.position[0]-x)**2) <= self.visibility**2:  # test in bounding circle
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
                while cellmap[(X*i)+self.position[0], self.position[1]].transparent and X < self.visibility:     # if transparent and within bounding range
                    visible.add(((X*i)+self.position[0], self.position[1]))
                    X += 1                                                              # move away from player
                visible.add(((X*i)+self.position[0], self.position[1]))                 # make final cell visible
            for i in (-1, 1):                                                           # Repeat as above, but vertically
                Y = 0
                while cellmap[self.position[0], (Y*i)+self.position[1]].transparent and Y < self.visibility:
                    visible.add((self.position[0], (Y*i)+self.position[1]))
                    Y += 1
                visible.add((self.position[0], (Y*i)+self.position[1]))

        diagonalcheck()
        crosscheck()
        return visible

    def detonate(self, cellmap):
        '''Detonate carried explosives at player's location'''
        if self.score[collectables.DYNAMITE] <= 0:
            return
        if not cellmap[self.position].destructable:
            return
        cellmap.detonate(self.position)
        self.score[collectables.DYNAMITE] -= 1
