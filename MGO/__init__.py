import glob, os, sys
import BaseMGO

GEMGOTYPES = []
# Hacky automagic importing of all MGO classes
# in lieu of a sane plugin system.
modfiles = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
modnames = [os.path.basename(file)[:-3] for file in modfiles]
for name in modnames:
    if name == "__init__" or name == "BaseMGO":
        continue
    mod = __import__(name, globals(), locals())
    modclass = getattr(mod, name)
    # At this point, we overwrite the loaded-module attribute
    # with the class of the same name. Because.
    setattr(sys.modules[__name__], name, modclass)
    if issubclass(modclass, BaseMGO.GEMGO):
        GEMGOTYPES.append(modclass)
