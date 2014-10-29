import random
import images
import MGO

def mindist(a, b, size):
    '''Distance between two values accounting for world wrapping'''
    return min((b-a)%size,(a-b)%size)

class Bear(MGO.GEMGO):
    '''Harmless animal that follows the player'''
    PER_TILE = 1/3000

    def __init__(self, position, cellmap):
        '''Create bear at position'''
        super(Bear, self).__init__(position, cellmap)
        self.direction = -1 # Left
        self.speed = 0.7    # Chance of moving per turn, max 1, min 0
        self.pfmapsize = 32
        self.detectionrange = 18
        self.hunting = False

    def directiontoplayer(self, playerpos):
        '''Find the best direction to move towards the player'''
        if (mindist(playerpos[0], self.position[0], self.cellmap.size[0]) > self.pfmapsize or
            mindist(playerpos[1], self.position[1], self.cellmap.size[1]) > self.pfmapsize):
            # Player is outside pathfinder area
            return False

        def mapcoord(pfcoord):
            '''Get map coordinate from pathfinder one'''
            return ((self.position[0] + pfcoord[0] - self.pfmapsize) % self.cellmap.size[0],
                    (self.position[1] + pfcoord[1] - self.pfmapsize) % self.cellmap.size[1])

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
                newdist = curdist+self.cellmap[mapcoord(nbrpos)]['difficulty']
                if ((dijkstramap[nbrpos[0]][nbrpos[1]][0] <= newdist and dijkstramap[nbrpos[0]][nbrpos[1]][0] != 0) or
                    self.cellmap[mapcoord(nbrpos)]['solid']):
                    continue
                dijkstramap[nbrpos[0]][nbrpos[1]] = [newdist, curpos, False]
                heapq.heappush(openlist, (newdist, nbrpos))
        if not foundtarget:
            return False
        while dijkstramap[curpos[0]][curpos[1]][1] != (self.pfmapsize, self.pfmapsize):
            curpos = dijkstramap[curpos[0]][curpos[1]][1]
        return [curpos[0]-self.pfmapsize,
                curpos[1]-self.pfmapsize]

    def update(self, playerpos):
        def chaseplayer():
            '''Decide whether to chase the player'''
            if (mindist(playerpos[0], self.position[0], self.cellmap.size[0])**2 +
                mindist(playerpos[1], self.position[1], self.cellmap.size[1])**2) > self.detectionrange**2:
                # Can't see/smell/hear (?) player
                return False
            if random.random() > self.speed:
                # Bored?
                return False
            return True

        def randommove():
            '''Move in random direction'''
            move = [0, random.randint(-1,1)]
            random.shuffle(move)
            return move

        washunting = self.hunting
        self.hunting = chaseplayer()
        if self.hunting:
            # Move in direction of player, or randomly if no path found.
            poschange = self.directiontoplayer(playerpos) or randommove()
            if washunting:
                self._suggestmessage("You are being chased by a bear", 1)
            else:
                self._suggestmessage("A bear starts chasing you", 2)
        else:
            # Move randomly.
            poschange = randommove()
            if washunting:
                self._suggestmessage("The bear has lost interest in you", 1)

        self.direction = poschange[0] if abs(poschange[0]) else self.direction
        newpos = ((self.position[0]+poschange[0]) % self.cellmap.size[0],
                  (self.position[1]+poschange[1]) % self.cellmap.size[1])

        if self.cellmap[newpos]['solid']:
            return False
        self.position = newpos
        return True

    def sprite(self):
        if self.cellmap[self.position]['visible']:
            return (images.BearRight if self.direction > 0 else images.BearLeft), self._pixelpos(2,2), 1
        else:
            return None
