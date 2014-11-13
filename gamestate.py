import os
import json
import threading
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

__worlds = {}

__states = [{
    'map': None,
    'world': None,
    'state': 'loading'
    }]

statelock = threading.Lock()

def getstate(state, part):
    with statelock:
        retval = __states[state][part]
    return retval

def setstate(state, partvalues):
    with statelock:
        for part, value in partvalues.iteritems():
            __states[state][part] = value

def bglworld(name):
    setstate(0, {'map': name,'state': 'loading'})
    __worlds[name] =  World(__mapdefs[name])
    setstate(0, {'map': name, 'world': __worlds[name], 'state': 'normal'})

def loadworld(name, blocking=False):
    global states
    if name not in __worlds:
        if blocking:
            __worlds[name] =  World(__mapdefs[name])
        else:
            t = threading.Thread(target=bglworld, args=[name])
            t.start()
            return False
    setstate(0, {'map': name, 'world': __worlds[name], 'state': 'normal'})

loadworld(config.get('map', 'initialmap', str), blocking=True)

def stepname(step):
    mapdefkeys = __mapdefs.keys()
    currentindex = mapdefkeys.index(getstate(0, 'map'))
    nextindex = currentindex + step
    return mapdefkeys[nextindex] if nextindex in range(len(mapdefkeys)) else None

def stepworld(step):
    name = stepname(step)
    if name is not None:
        loadworld(name)
