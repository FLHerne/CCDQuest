import pygame
import random
import collectables
import images
import coords
import MGO
from Map import Map
from colors import *

TILESIZE = images.TILESIZE

class World:
    def __init__(self, mapdict):
        self.mapdef = mapdict
        self.cellmap = Map(mapdict)

        self.gemgos = []
        for gemgo in MGO.GEMGOTYPES:
            self.gemgos += gemgo.place(self.cellmap)

    def insertgeplayer(self, geplayer):
        if geplayer not in self.gemgos:
            self.gemgos.append(geplayer)
        geplayer.updatevisible()
        self.rendervisible(geplayer)

    def removegeplayer(self, geplayer):
        self.gemgos.remove(geplayer)

    def rendervisible(self, geplayer, extrasprites=[]):
        sprites = []
        sprites += extrasprites

        for gemgo in self.gemgos:
            sprite = gemgo.sprite(geplayer)
            if sprite is not None:
                sprites.append(sprite)

        visibleranges = ([],[])
        for axis in [0, 1]:
            if 2*geplayer.visibility + 5 >= self.cellmap.size[axis]:
                visibleranges[axis].append((0, self.cellmap.size[axis]))
            else:
                rmin = (geplayer.position[axis] - geplayer.visibility - 2) % self.cellmap.size[axis]
                rmax = (geplayer.position[axis] + geplayer.visibility + 2) % self.cellmap.size[axis]
                if rmin < rmax:
                    visibleranges[axis].append((rmin, rmax))
                else:
                    visibleranges[axis].append((rmin, self.cellmap.size[axis]))
                    visibleranges[axis].append((0, rmax))

        surface = geplayer.surface
        for rx in visibleranges[0]:
            for ry in visibleranges[1]:
                surface.set_clip(
                    rx[0]*TILESIZE, ry[0]*TILESIZE,
                    (rx[1]-rx[0])*TILESIZE, (ry[1]-ry[0])*TILESIZE)
                regionsprites = sprites
                for ix in range(rx[0]-1, rx[1]+1):
                    for iy in range(ry[0]-1, ry[1]+1):
                        regionsprites += self.cellmap.sprites((ix, iy))
                        if coords.mod((ix, iy), self.cellmap.size) not in geplayer.visibletiles:
                            sprites.append((images.NonVisible, coords.sum(coords.mul((ix, iy), TILESIZE), (-4,-4)), 100))
                regionsprites.sort(key=lambda x: x[2])
                for sprite in regionsprites:
                    surface.blit(*sprite[:2])

    def update(self, geplayer):
        """Move the player by (x, y), move other fauna, update world surface around player"""
        self.cellmap.update()
        geplayer.updatevisible()

        self.players = filter(lambda x: isinstance(x, MGO.GEPlayer), self.gemgos)
        gemgosprites = []
        for gemgo in self.gemgos:
            gemgo.update(self)

        self.rendervisible(geplayer, gemgosprites)

        if geplayer.position in self.cellmap.burningtiles:
            geplayer.score[collectables.CHOCOLATE] -= Map.CELLBURNINGCOST
