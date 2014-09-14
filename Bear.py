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
        self.detectionrange = 18
        self.pfinitialvalue = (2*self.pfmapsize)**2

    def huntplayer(self, playerpos, cellmap):
        '''move towards the player'''
        if random.random() > self.speed:
            return False
        def mindist(a, b, size):
            '''distance between two values accounting for world wrapping'''
            return min((b-a)%size,(a-b)%size)
        if (mindist(playerpos[0], self.position[0], cellmap.size[0])**2 +
            mindist(playerpos[1], self.position[1], cellmap.size[1])**2) > self.detectionrange**2:
            return False
        def mapcoord(pfcoord):
            '''get map coordinate from pathfinder ones'''
            return ((self.position[0] + pfcoord[0] - self.pfmapsize) % cellmap.size[0],
                    (self.position[1] + pfcoord[1] - self.pfmapsize) % cellmap.size[1])

        foundtarget = False
        dijkstramap = [[(self.pfinitialvalue, (self.pfmapsize, self.pfmapsize)) for x in xrange(2*self.pfmapsize)] for x in xrange(2*self.pfmapsize)]
        import heapq
        openlist = []
        heapq.heappush(openlist, (0, (self.pfmapsize, self.pfmapsize)))
        curpos = None
        while openlist:
            curnode = heapq.heappop(openlist)
            curdist = curnode[0]
            curpos = curnode[1]
            if mapcoord(curpos) == tuple(playerpos):
                foundtarget = True
                break
            for nbrpos in [(curpos[0]-1, curpos[1]), (curpos[0], curpos[1]-1), (curpos[0]+1, curpos[1]), (curpos[0], curpos[1]+1)]:
                if nbrpos[0] < 0 or nbrpos[1] < 0 or nbrpos[0] >= 2*self.pfmapsize or nbrpos[1] >= 2*self.pfmapsize:
                    continue
                if dijkstramap[nbrpos[0]][nbrpos[1]][0] != self.pfinitialvalue or cellmap[mapcoord(nbrpos)].solid:
                    continue
                dijkstramap[nbrpos[0]][nbrpos[1]] = (curdist+1, curpos)
                heapq.heappush(openlist, (curdist+1, nbrpos))
        if not foundtarget:
            return False
        while dijkstramap[curpos[0]][curpos[1]][1] != (self.pfmapsize, self.pfmapsize):
            curpos = dijkstramap[curpos[0]][curpos[1]][1]
        self.position[0] = (self.position[0]+curpos[0]-self.pfmapsize)%cellmap.size[0]
        self.direction = curpos[0]-self.pfmapsize if abs(curpos[0]-self.pfmapsize) else self.direction
        self.position[1] = (self.position[1]+curpos[1]-self.pfmapsize)%cellmap.size[1]
        return True

    def sprite(self):
        return images.BearRight if self.direction > 0 else images.BearLeft
