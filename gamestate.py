import os
import json
import config
from World import World

__mapdefs = {}
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
    __mapdefs[name] = newmap
if not len(__mapdefs):
    raise Exception("No loadable maps!")

currentmap = config.get('map', 'initialmap', str)
currentworld = World(__mapdefs[currentmap])

def loadworld(name):
    global currentmap
    global currentworld
    currentmap = name
    currentworld = World(__mapdefs[currentmap])

def stepname(step):
    mapdefkeys = __mapdefs.keys()
    currentindex = mapdefkeys.index(currentmap)
    nextindex = currentindex + step
    return mapdefkeys[nextindex] if nextindex in range(len(mapdefkeys)) else None