import pygame
import random
import collectables
import images
import coords
from MGO import *
import Player
from Map import Map
from colors import *

TILESIZE = images.TILESIZE

class World:
    def __init__(self, mapdef):
        self.cellmap = Map(mapdef)
        self.surfaces = {}
        self.mapdef = mapdef

        self.gemgos = []
        for gemgo in BaseMGO.GEMGO.__subclasses__():
            self.gemgos += gemgo.place(self.cellmap)
        self.players = []

    def insertplayer(self, player):
        self.players.append(player)
        self.surfaces[player] = pygame.Surface(coords.mul(self.cellmap.size, TILESIZE))
        bgtile = images.Unknown.copy()
        bgtile.blit(images.NonVisible, (0, 0))
        surface = self.surfaces[player]
        for ix in xrange(0, self.cellmap.size[0]*TILESIZE, TILESIZE):
            for iy in xrange(0, self.cellmap.size[1]*TILESIZE, TILESIZE):
                surface.blit(bgtile, (ix, iy))

    def removeplayer(self, player):
        self.players.remove(player)
        self.surfaces[player] = None

    def rendervisibletiles(self, player, extrasprites=[]):
        player.updatevisible()
        for tile in player.visibletiles:
            cell = self.cellmap[tile]
            cell['explored'] = True
        if not self.cellmap[player.position]['transparent']:
            player.visibletiles.remove(player.position)
        sprites = extrasprites

        visibleranges = ([],[])
        for axis in [0, 1]:
            if 2*player.visibility + 5 >= self.cellmap.size[axis]:
                visibleranges[axis].append((0, self.cellmap.size[axis]))
            else:
                rmin = (player.position[axis] - player.visibility - 2) % self.cellmap.size[axis]
                rmax = (player.position[axis] + player.visibility + 2) % self.cellmap.size[axis]
                if rmin < rmax:
                    visibleranges[axis].append((rmin, rmax))
                else:
                    visibleranges[axis].append((rmin, self.cellmap.size[axis]))
                    visibleranges[axis].append((0, rmax))

        surface = self.surfaces[player]
        for rx in visibleranges[0]:
            for ry in visibleranges[1]:
                surface.set_clip(
                    rx[0]*TILESIZE, ry[0]*TILESIZE,
                    (rx[1]-rx[0])*TILESIZE, (ry[1]-ry[0])*TILESIZE)
                regionsprites = sprites
                for ix in range(rx[0]-1, rx[1]+1):
                    for iy in range(ry[0]-1, ry[1]+1):
                        regionsprites += self.cellmap.sprites((ix, iy))
                        if coords.mod((ix, iy), self.cellmap.size) not in player.visibletiles:
                            sprites.append((images.NonVisible, coords.mul((ix, iy), TILESIZE), 100))
                regionsprites.sort(key=lambda x: x[2])
                for sprite in regionsprites:
                    surface.blit(*sprite[:2])

    def moveplayer(self, player, arg):
        """Move the player by (x, y), move other fauna, update world surface around player"""
        self.cellmap.update()
        player.action(arg)

        gemgosprites = []
        for gemgo in self.gemgos:
            gemgo.update(self)
            sprite = gemgo.sprite(player)
            if sprite is not None:
                gemgosprites.append(sprite)
        playersprites = [iterplayer.sprite(player) for iterplayer in self.players]
        playersprites = filter(lambda x: x is not None, playersprites)

        self.rendervisibletiles(player, gemgosprites+playersprites)

        if player.position in self.cellmap.burningtiles:
            player.score[collectables.CHOCOLATE] -= Map.CELLBURNINGCOST
