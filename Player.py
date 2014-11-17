import threading
import collectables
import config
import worlds
from MGO.GEPlayer import GEPlayer

class Player(object):
    def __init__(self):
        self.geplayer = None
        self.statelock = threading.Lock()
        self.state = 'normal'
        self.mapdef = None
        self.score = {
            collectables.COIN: 0,
            collectables.CHOCOLATE: 10000,
            collectables.DYNAMITE: 15
        }
        self.setworld(config.get('map', 'initialmap', str), blocking=True)

    def setworld(self, name, position=None, blocking=False):
        with self.statelock:
            if self.state != 'normal':
                return False
            self.state = 'loading'
            self.mapdef = worlds.mapdefs[name]
        if self.geplayer is not None:
            self.geplayer.world.removegeplayer(self.geplayer)
        def lworld():
            geplayer = GEPlayer(self, worlds.getworld(name), position)
            with self.statelock:
                self.geplayer = geplayer
                self.state = 'normal'
        t = threading.Thread(target=lworld)
        t.start()
        if blocking:
            t.join()

    def stepworld(self, step):
        nextname = worlds.stepname(self.geplayer.world.mapdef['dir'], step) #FIXME
        if nextname:
            self.setworld(nextname)

    def action(self, arg):
        if self.state != 'normal':
            return  False
        self.geplayer.action(arg)
        self.score = self.geplayer.score
        if self.score[collectables.CHOCOLATE] <= 0:
            self.state = 'lost'
