import ConfigParser
import os.path
import json

mainconfig = ConfigParser.RawConfigParser()
loaded = mainconfig.read("CCDQuest.cfg")
if not loaded:
    raise Exception("Failed to load CCDQuest.cfg!")

def get(section, name, valuetype, default=None):
    try:
        if valuetype is bool:
            # ConfigParser.getboolean() does useful string parsing.
            return mainconfig.getboolean(section, name)
        else:
            return valuetype(mainconfig.get(section, name))
    except ValueError:
        if default is None:
            raise
        else:
            print "Warning: invalid value for ["+section+"] '"+name+"'"
    except ConfigParser.Error:
        if default is None:
            raise
    return valuetype(default)

maps = []
for im in mainconfig.items("maps"):
    descfilename = os.path.join('map', im[1], 'mapdesc.json')
    try:
        imfile = open(descfilename)
    except:
        print "Unable to load map", im[0]+":"
        print "File", descfilename, "unreadable or missing"
        continue
    try:
        newmap = json.load(imfile)
    except ValueError as err:
        print "Unable to load map", im[0]+":"
        print err
        continue
    imfile.close()
    newmap['dir'] = im[1]
    maps.append(newmap)
if not len(maps):
    raise Exception("No loadable maps!")
