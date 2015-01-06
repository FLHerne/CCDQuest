import pygame
import random
import images
import BaseMGO
import collectables
from colors import *
import coords
import config
from directions import *
TILESIZE = images.TILESIZE

class GEPlayer(BaseMGO.GEMGO):
    """The player, exploring the grid-based world"""
    FREEPLAYER = config.get('player', 'freeplayer', bool, False)
    XRAYVISION = config.get('player', 'xrayvision', bool, False)
    POSMESSAGE = config.get('player', 'posmessage', bool, False)

    def __init__(self, player, world, position):
        """Initialise instance variables"""
        self.player = player
        self.score = player.score
        self.world = world
        position = position if position else world.cellmap.startpos
        super(GEPlayer, self).__init__(position, world.cellmap)
        self.color = MAGENTA
        self.visibility = 15
        self.direction = RIGHT
        self.surface = pygame.Surface(coords.mul(world.cellmap.size, TILESIZE))
        self.surface.fill(BLACK)
        #bgtile = images.Unknown.copy()
        #bgtile.blit(images.NonVisible, (0, 0))
        #for ix in xrange(0, world.cellmap.size[0]*TILESIZE, TILESIZE):
        #    for iy in xrange(0, world.cellmap.size[1]*TILESIZE, TILESIZE):
        #        self.surface.blit(bgtile, (ix, iy))
        self.setup()

    def setup(self):
        self.layingfuse = False
        self.visibletiles = set()
        self.pendingteleports = []
        self.world.insertgeplayer(self)

    @classmethod
    def place(cls, cellmap):
        return []

    def update(self, world):
        if GEPlayer.POSMESSAGE:
            self._suggestmessage(str(self.position), 1)

    def sprite(self, player):
        if self.position in player.visibletiles:
            image = images.PlayerRight if self.direction == RIGHT else images.PlayerLeft
            return self._pokedsprite(image, layer=0)

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
        elif arg in CARDINALS:
            self.move(*arg)
        self.world.update(self)
        if self.pendingteleports:
            teleport = random.choice(self.pendingteleports)
            if teleport[0] == self.world.mapdef['name']:
                self.position = tuple(teleport[1])
                self.setup()
            else:
                self.player.setworld(*random.choice(self.pendingteleports))

    def move(self, x, y):
        """Move if possible, update collectable levels accordingly"""
        if abs(x) + abs(y) != 1:
            return False
        self.direction = (x, y)
        if self.cellmap[coords.sum(self.position, (x, y))]['solid'] and not GEPlayer.FREEPLAYER:
            self.score[collectables.CHOCOLATE] -= 50
            return False
        self.position = coords.modsum(self.position, self.direction, self.cellmap.size)
        collectable = self.cellmap[self.position]['collectableitem']
        if collectable != 0:
            self.score[collectable] += collectables.value[collectable]
            self._suggestmessage("You pick up " + collectables.name[collectable], 4)
        self.cellmap[self.position]['collectableitem'] = 0
        if not GEPlayer.FREEPLAYER:
            self.score[collectables.CHOCOLATE] -= self.terraincost()
        if self.layingfuse and self.cellmap[self.position]['sogginess'] < 25:
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
        """Detonate carried explosives at player's location"""
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

    def delayedteleport(self, worldname, position=None):
        self.pendingteleports.append((worldname, position))

    def terraincost(self):
        """Determine cost of moving onto a cell"""
        cell = self.cellmap[self.position]
        cost = 3.0 if not cell['transparent'] else 1.0
        cost += float(abs(cell['temperature'] - 20)) / 8
        cost += float(cell['sogginess']) / 8
        cost += float(cell['roughness']) / 16
        return cost

    def updatevisible(self):
        """Calculate and return the set of tiles visible to player"""
        self.visibletiles = set()
        self.visibletiles.add(self.position)

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
                        if not GEPlayer.XRAYVISION and not self.cellmap[branchpos]['transparent']:
                            break
                        branchpos = coords.sum(branchpos, diagdir)
                if not GEPlayer.XRAYVISION and not self.cellmap[trunkpos]['transparent']:
                    break
                trunkpos = coords.sum(trunkpos, outdir)

        for tile in self.visibletiles:
            cell = self.cellmap[tile]
            cell['explored'] = True
        if not self.cellmap[self.position]['transparent']:
            self.visibletiles.remove(self.position)
