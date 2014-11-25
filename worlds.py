import json
import os
from World import World

mapdefs = {}
for name in os.listdir('map'):
    if not os.path.isdir(os.path.join('map', name)):
        continue
    descfilename = os.path.join('map', name, 'mapdesc.json')
    try:
        imfile = open(descfilename)
    except:
        print "Unable to load map", name+":"
        print "File", descfilename, "unreadable or missing"
        continue
    try:
        newmap = json.load(imfile)
    except ValueError as err:
        print "Unable to load map", name+":"
        print err
        continue
    imfile.close()
    newmap['dir'] = name
    mapdefs[name] = newmap
if not len(mapdefs):
    raise Exception("No loadable maps!")

class PortalException(Exception):
    """Exception for invalid portal definitions"""
    def __init__(self, portalpos, portaldest):
        posstr = ', '.join(repr(e) for e in portalpos)
        if portaldest is None:
            message = "Portal at %s has no connections." %posstr
        else:
            deststr = ', '.join(repr(e) for e in portaldest)
            message = "Portal from %s to %s is unterminated." %(posstr, deststr)
        Exception.__init__(self, message)

def __checkportals():
    """Validate portal relationships"""
    postodest = {}
    for mapname, portaldefs in [(mapdef['dir'], mapdef['gemgos']['portals']) for mapdef in mapdefs.values()]:
        for portaldef in portaldefs:
            pos  = (mapname, tuple(portaldef[0]))
            dest = (str(portaldef[1]), tuple(portaldef[2])) if len(portaldef) >= 3 else None
            postodest[pos] = dest

    # Check that all portals without incoming connections link somewhere themselves.
    for nonreceiver in set(postodest.keys()).difference(postodest.values()):
        if postodest[nonreceiver] is None:
            raise PortalException(nonreceiver, None)

    # Check that the destination of each portal is another portal.
    desttopos = dict((b,a) for a, b in postodest.items())
    for nondest in set(postodest.values()).difference(postodest.keys()):
        if nondest is not None:
            raise PortalException(desttopos[nondest], nondest)

__checkportals()

__worlds = {}

def getworld(name):
    if name not in __worlds:
        __worlds[name] = World(mapdefs[name])
    return __worlds[name]

def stepname(curname, step):
    mapdefkeys = mapdefs.keys()
    currentindex = mapdefkeys.index(curname)
    nextindex = currentindex + step
    return mapdefkeys[nextindex] if nextindex in range(len(mapdefkeys)) else None
