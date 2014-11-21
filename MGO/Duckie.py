import images
import coords
import random
import config
import BaseMGO

class Duckie(BaseMGO.GEMGO):
    """Duckie that wanders around"""
    PER_TILE = 1/config.get('fauna', 'tiles_per_duckie', float, 250)
    
    def __init__(self, position, cellmap):
        """Create new duckie in position"""
        super(Duckie, self).__init__(position, cellmap)
        self.direction = -1 # Left
        self.visible = False

    #@classmethod
    #def place(cls, cellmap):
    #    created = []
    #    if 'duckies' in cellmap.gemgodefs:
    #        for duckiedef in cellmap.gemgodefs['duckies']:
    #            created.append(cls(duckiedef[1], duckiedef[0], cellmap))
    #    return created

    def update(self, world):
        """DOCSTRING NEEDED HERE"""
        self.move()
        nearbytiles = coords.neighbours(self.position) + [self.position]
        for player in world.players:
            if player.position in nearbytiles:
                self._suggestmessage("Quack", 15)
            if self.position in player.visibletiles:
                if not self.visible:
                    self._suggestmessage("Oh look, a duckie", 1)
                self.visible = True
            else:
                self.visible = False

    def move(self):

        def randommove():
            """Move in random direction"""
            move = [0, random.randint(-1,1)]
            random.shuffle(move)
            return move

        poschange = randommove()

        self.direction = poschange[0] if abs(poschange[0]) else self.direction
        newpos = coords.modsum(self.position, poschange, self.cellmap.size)

        if self.cellmap[newpos]['solid']:
            return False
        self.position = newpos
        return True

    def sprite(self, player):
        if self.position in player.visibletiles:
            if random.getrandbits(1):
                return images.DuckieLeft, self._pixelpos(), -1
            else:
                return images.DuckieRight, self._pixelpos(), -1

        else:
            return None



