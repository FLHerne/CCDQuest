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

def __checkportals():
    portallocs = set()  # Locations (mapname, coord) of all portals
    portaldests = set() # Destinations (mapname, coord) of all portals
    outportals = {}     # Index of portals that have destinations.

    for mapname, portaldefs in [(mapdef['dir'], mapdef['gemgos']['portals']) for mapdef in mapdefs.values()]:
        for portaldef in portaldefs:
            portallocs.add((mapname, tuple(portaldef[0])))
            if len(portaldef) >= 3:
                portaldests.add((portaldef[1], tuple(portaldef[2])))
                outportals[(mapname, tuple(portaldef[0]))] = True

    unterminated = portaldests.difference(portallocs)
    if unterminated:
        raise Exception("Portals at " + str(list(unterminated)) + " are unterminated.")

    # Check that all portals without incoming connections link somewhere themselves.
    for nonreceiver in portallocs.difference(portaldests):
        if nonreceiver not in outportals:
            raise Exception("Portal at " + str(nonreceiver) + " has no connections!")

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
