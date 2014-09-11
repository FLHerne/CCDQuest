import images
import random

class Bear:
    '''follows you around when in range'''
    def __init__(self, position):
        '''setup bear in given position'''
        self.position = list(position)
        self.direction = -1 # Left
        self.speed = 0.7         # Chance of moving per turn, max 1, min 0
        self.pfmapsize = 32
        self.detectionrange = 15
        self.pfinitialvalue = (2*self.pfmapsize)**2

    def huntplayer(self, playerpos, cellmap):
        '''move towards the player'''
        if random.random() > self.speed:
            return False
        def mindist(a, b, size):
            '''distance between two values accounting for world wrapping'''
            return min((b-a)%size,(a-b)%size)
        if (mindist(playerpos[0], self.position[0], cellmap.size[0]) +
            mindist(playerpos[1], self.position[1], cellmap.size[1])) > self.detectionrange:
            return False
        def mapcoord(d_coord):
            '''get map coordinate from pathfinder ones'''
            return ((self.position[0] + d_coord[0] - self.pfmapsize) % cellmap.size[0],
                    (self.position[1] + d_coord[1] - self.pfmapsize) % cellmap.size[1])

        foundtarget = False
        dijkstramap = [[(self.pfinitialvalue, (self.pfmapsize, self.pfmapsize)) for x in xrange(2*self.pfmapsize)] for x in xrange(2*self.pfmapsize)]
        import heapq
        openlist = []
        heapq.heappush(openlist, (0, (self.pfmapsize, self.pfmapsize)))
        curp = False
        while openlist:
            curn = heapq.heappop(openlist)
            curd = curn[0]
            curp = curn[1]
            if mapcoord(curp) == tuple(playerpos):
                foundtarget = True
                break
            for nbrpos in [(curp[0]-1, curp[1]), (curp[0], curp[1]-1), (curp[0]+1, curp[1]), (curp[0], curp[1]+1)]:
                if nbrpos[0] < 0 or nbrpos[1] < 0 or nbrpos[0] >= 2*self.pfmapsize or nbrpos[1] >= 2*self.pfmapsize:
                    continue
                if dijkstramap[nbrpos[0]][nbrpos[1]][0] != self.pfinitialvalue or cellmap[mapcoord(nbrpos)].solid:
                    continue
                dijkstramap[nbrpos[0]][nbrpos[1]] = (curd+1, curp)
                heapq.heappush(openlist, (curd+1, nbrpos))
        if not foundtarget:
            return False
        while dijkstramap[curp[0]][curp[1]][1] != (self.pfmapsize, self.pfmapsize):
            curp = dijkstramap[curp[0]][curp[1]][1]
        self.position[0] = (self.position[0]+curp[0]-self.pfmapsize)%cellmap.size[0]
        self.direction = curp[0]-self.pfmapsize if abs(curp[0]-self.pfmapsize) else self.direction
        self.position[1] = (self.position[1]+curp[1]-self.pfmapsize)%cellmap.size[1]
        return True
    
    def sprite(self):
        return images.BearRight if self.direction > 0 else images.BearLeft
