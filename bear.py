include pygame

class Bear():
    def __init__(self, position):
        '''setup bear in given position'''
        self.position = list(position)
        self.direction = -1                 # Facing left
    def move():
        pass
    def draw(self, drawSurface):
        '''Blit self to specified surface'''
        if RealMap[self.position].top or not RealMap[self.position].visible:
            return
        x = ((self.position[0]*BLOCKSIZE))
        y = ((self.position[1]*BLOCKSIZE))
        drawSurface.blit(images.BearRight if self.direction > 0 else images.BearLeft, (x, y))
        
    def hunt(self):
        '''move towards the player'''
        if abs(Pos[0]-self.position[0]) + abs(Pos[1]-self.position[1]) > 15:
            return False
        def worldPos(d_coord):
            return (self.position[0] + d_coord[0] - 32,
                    self.position[1] + d_coord[1] - 32)
        def isTarget(d_coord):
            return (worldPos(d_coord)[0]%worldSize[0] == Pos[0]%worldSize[0] and
                    worldPos(d_coord)[1]%worldSize[1] == Pos[1]%worldSize[1])

        foundtarget = False
        dijkstramap = [[(512, (32, 32)) for x in xrange(64)] for x in xrange(64)]
        import heapq
        openlist = []
        heapq.heappush(openlist, (0, (32, 32)))
        curp = False
        while openlist:
            curn = heapq.heappop(openlist)
            curd = curn[0]
            curp = curn[1]
            #print "CurP is", curp
            if isTarget(curp):
                foundtarget = True
                break
            for nbrpos in [(curp[0]-1, curp[1]), (curp[0], curp[1]-1), (curp[0]+1, curp[1]), (curp[0], curp[1]+1)]:
                if nbrpos[0] < 0 or nbrpos[1] < 0 or nbrpos[0] >= 64 or nbrpos[1] >= 64:
                    continue
                if dijkstramap[nbrpos[0]][nbrpos[1]][0] != 512 or RealMap[worldPos(nbrpos)].solid:
                    continue
                dijkstramap[nbrpos[0]][nbrpos[1]] = (curd+1, curp)
                heapq.heappush(openlist, (curd+1, nbrpos))
        if not foundtarget:
            DebugPrint("Bear pathfinder failed")
            return False
        DebugPrint("Bear pathfinder succeeded")
        while dijkstramap[curp[0]][curp[1]][1] != (32, 32):
            curp = dijkstramap[curp[0]][curp[1]][1]
        self.position[0] += curp[0]-32
        self.direction = curp[0]-32 if abs(curp[0]-32) else self.direction
        self.position[1] += curp[1]-32
        return True