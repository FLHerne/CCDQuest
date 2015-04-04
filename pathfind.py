import coords

def firstmove(startpos, destpos, costs, cellmap, pfmapsize=15, maxcost=40):
    """Find the best direction to move towards the destination"""

    if (any(ax > pfmapsize for ax in coords.mindist(startpos, destpos, cellmap.size))):
        # Player is outside pathfinder area
        return False

    def mapcoord(pfcoord):
        """Get map coordinate from pathfinder one"""
        return coords.modsum(startpos, pfcoord, (-pfmapsize,)*2, cellmap.size)

    foundtarget = False
    dijkstramap = [[[0, (pfmapsize,)*2, False] for x in xrange(2*pfmapsize)] for x in xrange(2*pfmapsize)]
    import heapq
    openlist = []
    heapq.heappush(openlist, (0, (pfmapsize,)*2))
    curpos = None
    while openlist:
        curnode = heapq.heappop(openlist)
        curdist = curnode[0]
        if curdist > maxcost:
            # Give up if player is painfully unreachable.
            break
        curpos = curnode[1]
        if mapcoord(curpos) == tuple(destpos):
            foundtarget = True
            break
        if dijkstramap[curpos[0]][curpos[1]][2] == True:
            continue
        else:
            dijkstramap[curpos[0]][curpos[1]][2] = True
        for nbrpos in coords.neighbours(curpos):
            if (nbrpos[0] < 0 or nbrpos[1] < 0 or
                nbrpos[0] >= 2*pfmapsize or nbrpos[1] >= 2*pfmapsize or
                nbrpos == (pfmapsize, pfmapsize)):
                continue
            cellcost = costs(cellmap[mapcoord(nbrpos)])
            newdist = curdist+cellcost
            if ((dijkstramap[nbrpos[0]][nbrpos[1]][0] <= newdist and dijkstramap[nbrpos[0]][nbrpos[1]][0] != 0) or
                cellmap[mapcoord(nbrpos)]['solid'] or cellcost > 8):
                continue
            dijkstramap[nbrpos[0]][nbrpos[1]] = [newdist, curpos, False]
            heapq.heappush(openlist, (newdist, nbrpos))
    if not foundtarget:
        return False
    while dijkstramap[curpos[0]][curpos[1]][1] != (pfmapsize, pfmapsize):
        curpos = dijkstramap[curpos[0]][curpos[1]][1]
    return coords.sum(curpos, (-pfmapsize,)*2)
