import random

import coords
import images
import pathfind
import BaseMGO

class PortalGuard(BaseMGO.GEMGO):
    viewradius = 10
    maxportaldist = 10
    def __init__(self, position, cellmap):
        """Create portal guard on a portal"""
        super(PortalGuard, self).__init__(position, cellmap)
        self.position = position
        self.portalpos = position

    @classmethod
    def place(cls, cellmap):
        """Guard ALL the portals!"""
        created = []
        if 'portals' in cellmap.gemgodefs:
            for portaldef in cellmap.gemgodefs['portals']:
                created.append(cls(portaldef[0], cellmap))
        return created

    @staticmethod
    def terraincost(cell):
        if (cell['solid']) or (cell['sogginess'] == 100):
            return 100
        else:
            return 1

    def update(self, world):
        self.visibletiles = BaseMGO.visibletiles(self.position, self.cellmap,
                                                 PortalGuard.viewradius)
        nearbyplayers = filter(lambda p: p.position in self.visibletiles, world.players)
        if not nearbyplayers:
            move = pathfind.firstmove(self.position, self.portalpos, PortalGuard.terraincost,
                                      self.cellmap)
            newpos = coords.sum(self.position, move)
            portaldist = coords.mindist(newpos, self.portalpos, self.cellmap.size)
            if (sum(ax**2 for ax in portaldist) > self.maxportaldist**2):
                return
            self.position = newpos
        else:
            def playerportaldist(player):
                return sum(coords.mindist(player.position, self.portalpos, self.cellmap.size))
            targetpos = sorted(nearbyplayers, key=playerportaldist)[0].position
            offset = coords.tileoffset(self.position, targetpos, self.cellmap.size)
            newpos = coords.sum(self.position, [cmp(ax,0) for ax in offset])
            if self.cellmap[newpos]['solid']:
                return
            portaldist = coords.mindist(newpos, self.portalpos, self.cellmap.size)
            if (sum(ax**2 for ax in portaldist) > self.maxportaldist**2):
                return
            self.position = newpos

    def sprite(self, player):
        if self.position in player.visibletiles:
            image = images.PixieLeft
            return self._pokedsprite(image)

        else:
            return None
