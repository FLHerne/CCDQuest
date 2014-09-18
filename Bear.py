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
        dijkstramap = [[[0, (self.pfmapsize, self.pfmapsize), False] for x in xrange(2*self.pfmapsize)] for x in xrange(2*self.pfmapsize)]
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
            if dijkstramap[curpos[0]][curpos[1]][2] == True:
                continue
            else:
                dijkstramap[curpos[0]][curpos[1]][2] = True
            for nbrpos in [(curpos[0]-1, curpos[1]), (curpos[0], curpos[1]-1), (curpos[0]+1, curpos[1]), (curpos[0], curpos[1]+1)]:
                if (nbrpos[0] < 0 or nbrpos[1] < 0 or
                    nbrpos[0] >= 2*self.pfmapsize or nbrpos[1] >= 2*self.pfmapsize or
                    nbrpos == (self.pfmapsize, self.pfmapsize)):
                    continue
                newdist = curdist+cellmap[mapcoord(nbrpos)].difficulty
                if ((dijkstramap[nbrpos[0]][nbrpos[1]][0] <= newdist and dijkstramap[nbrpos[0]][nbrpos[1]][0] != 0) or
                    cellmap[mapcoord(nbrpos)].solid):
                    continue
                dijkstramap[nbrpos[0]][nbrpos[1]] = [newdist, curpos, False]
                heapq.heappush(openlist, (newdist, nbrpos))
        if not foundtarget:
            return False
        while dijkstramap[curpos[0]][curpos[1]][1] != (self.pfmapsize, self.pfmapsize):
            curpos = dijkstramap[curpos[0]][curpos[1]][1]
        return [curpos[0]-self.pfmapsize,
                curpos[1]-self.pfmapsize]

    def move(self, playerpos, cellmap):
        poschange = self.huntplayer(playerpos, cellmap)
        if poschange == False:
            poschange = [0, random.randint(-1,1)]
            random.shuffle(poschange)
        newpos = ((self.position[0]+poschange[0]) % cellmap.size[0],
                  (self.position[1]+poschange[1]) % cellmap.size[1])
        if cellmap[newpos].solid:
            return False
        self.direction = poschange[0] if abs(poschange[0]) else self.direction
        self.position = newpos
        return True

    def sprite(self):
        return images.BearRight if self.direction > 0 else images.BearLeft
