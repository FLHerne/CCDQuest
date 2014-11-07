import pygame
import random
import images
from images import TILESIZE
import MGO
import collectables
from colors import *
import coords
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
        self.visibletiles = set()
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

    def sprite(self, player):
        if tuple(self.position) in player.visibletiles:
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
        elif arg == 'scattercoins':
            self.scattercoins(3, 10)
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
        self.position = coords.mod(coords.sum(self.position, self.direction), self.cellmap.size)
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
            return coords.sum(a, coords.mul(b, -1))
        oldpos = subtuple(self.position, self.direction)
        pathnbrs = []
        for nbrpos in coords.neighbours(self.position):
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

    def scattercoins(self, radius, number):
        sqradius = radius**2
        scattered = 0
        attempts = 0
        while scattered < number and attempts < 6*number and self.score[collectables.COIN] > 0:
            attempts += 1
            tryoffset = random.randint(-radius, radius), random.randint(-radius, radius)
            if tryoffset[0]**2 + tryoffset[1]**2 > sqradius:
                continue
            trypos = coords.sum(self.position, tryoffset)
            if self.cellmap[trypos]['collectableitem'] or self.cellmap[trypos]['solid']:
                continue
            self.cellmap[trypos]['collectableitem'] = collectables.COIN
            self.score[collectables.COIN] -= 1
            scattered += 1

    def updatevisible(self):
        '''Calculate and return the set of tiles visible to player'''
        self.visibletiles = set()
        self.visibletiles.add(tuple(self.position))

        def inrange(a):
            return ((a[0]-self.position[0])**2 + (a[1]-self.position[1])**2 < self.visibility**2)
        for outdir in CARDINALS:
            trunkpos = self.position
            while inrange(trunkpos):
                self.visibletiles.add(coords.mod(trunkpos, self.cellmap.size))
                for perpdir in perpendiculars(outdir):
                    diagdir = coords.sum(outdir, perpdir)
                    branchpos = trunkpos
                    while inrange(branchpos):
                        self.visibletiles.add(coords.mod(branchpos, self.cellmap.size))
                        if not Player.XRAYVISION and not self.cellmap[branchpos]['transparent']:
                            break
                        branchpos = coords.sum(branchpos, diagdir)
                if not Player.XRAYVISION and not self.cellmap[trunkpos]['transparent']:
                    break
                trunkpos = coords.sum(trunkpos, outdir)
