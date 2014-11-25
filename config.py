import ConfigParser
import os.path
import json

mainconfig = ConfigParser.RawConfigParser()
loaded = mainconfig.read("CCDQuest.cfg")
if not loaded:
    raise Exception("Failed to load CCDQuest.cfg!")

def get(section, name, valuetype, default=None):
    try:
        value = mainconfig.get(section, name)
        if valuetype is bool:
            # ConfigParser.getboolean() does useful string parsing.
            return mainconfig.getboolean(section, name)
        else:
            return valuetype(value)
    except ValueError:
        if default is None:
            raise
        else:
            print "Warning: invalid value '%s' for [%s], %s" %(value, section, name)
    except ConfigParser.Error:
        if default is None:
            raise
    return valuetype(default)
