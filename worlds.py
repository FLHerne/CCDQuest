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
