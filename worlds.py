import json
import os
from World import World

mapdefs = {}
for name in os.listdir('map'):
    if not os.path.isdir(os.path.join('map', name)):
        continue
    descfilename = os.path.join('map', name, name+'.json')
    try:
        imfile = open(descfilename)
    except:
        print "Unable to load map %s name:" %name
        print "File %s unreadable or missing" %descfilename
        continue
    try:
        newmap = json.load(imfile)
    except ValueError as err:
        print "Unable to load map %s:" %name
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

def __procportals():
    """Reorganise portal definiteions and validate portal relationships"""
    posindexed = {}
    for mapname in mapdefs.keys():
        portaldefs = mapdefs[mapname]['gemgos']['portals']
        for portaldef in portaldefs:
            pos  = (mapname, tuple(portaldef[0]))
            dest = (str(portaldef[1]), tuple(portaldef[2])) if len(portaldef) >= 3 else None
            posindexed[pos] = [dest, False, False]
        mapdefs[mapname]['gemgos']['portals'] = []

    for pos, pdef in posindexed.items():
        if pdef[0] is not None:
            if pdef[0] not in posindexed:
                raise PortalException(pos, pdef[0])
            if pos[0] == pdef[0][0]:
                posindexed[pdef[0]][1] = True
            else:
                posindexed[pdef[0]][2] = True

    for pos, pdef in posindexed.items():
        if not any(pdef):
            raise PortalException(pos, None)
        mapdefs[pos[0]]['gemgos']['portals'].append((pos[1],) + tuple(pdef))

__procportals()

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
