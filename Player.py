import collectables
import config
import worlds
from MGO.GEPlayer import GEPlayer

class Player(object):
    def __init__(self):
        self.geplayer = None
        self.score = {
            collectables.COIN: 0,
            collectables.CHOCOLATE: 10000,
            collectables.DYNAMITE: 15
        }
        self.setworld(config.get('map', 'initialmap', str))

    def setworld(self, name, position=None):
        if self.geplayer is not None:
            world = self.geplayer.world
            world.removegeplayer(self.geplayer)
        world = worlds.getworld(name)
        self.geplayer = GEPlayer(self, world)

    def action(self, arg):
        self.geplayer.action(arg)
        self.score = self.geplayer.score
