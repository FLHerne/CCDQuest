import random
from directions import *
import images
import coords
import config
import BaseMGO

class Dragon(BaseMGO.GEMGO):
    """Harmless flying thing that follows the player"""
    PER_TILE = 1/config.get('fauna', 'tiles_per_dragon', float, 25000)
    detectionrange = 18
    speed = 0.8

    def __init__(self, position, cellmap):
        """Create new dragon in position"""
        super(Dragon, self).__init__(position, cellmap)
        self.direction = UPLEFT
        self.hunting = None

    def update(self, world):
        """Fly toward the player if nearby, or continue in same direction"""
        def flameplayer():
            fronttiles = [coords.sum(self.position, coords.mul(self.direction, i)) for i in range(1,4)]
            for tile in fronttiles:
                if tile in [player.position for player in world.players]:
                    self._suggestmessage("The dragon breaths a jet of fire towards you", 5)
                    for tile in fronttiles:
                        self.cellmap.ignite(tile, forceignite=True)
                    break

        washunting = self.hunting
        self.hunting = None
        for player in world.players:
            playerpos = player.position
            if not self.cellmap[playerpos]['covered'] and random.random() < Dragon.speed:
                offset = coords.tileoffset(self.position, playerpos, self.cellmap.size)
                if offset[0]**2 + offset[1]**2 <= Dragon.detectionrange**2:
                    self.hunting = player
        if self.hunting:
            newdirection = list(self.direction)
            if abs(offset[0]) > abs(offset[1]):
                newdirection[0] = cmp(offset[0], 0)
            elif abs(offset[1]) > abs(offset[0]):
                newdirection[1] = cmp(offset[1], 0)
            elif cmp(offset[0], 0) != cmp(newdirection[0], 0):
                newdirection[0] = -self.direction[0]
            elif cmp(offset[1], 0) != cmp(newdirection[1], 0):
                newdirection[1] = -self.direction[1]
            self.direction = tuple(newdirection)
            if washunting:
                self._suggestmessage("You are being hunted down by a dragon", 2)
            else:
                self._suggestmessage("A dragon begins to chase you", 3)
        else:
            if washunting:
                self._suggestmessage("The dragon starts to fly away", 1)

        self.position = coords.modsum(self.position, self.direction, self.cellmap.size)
        flameplayer()

    @classmethod
    def place(cls, cellmap):
        """Create dragons in random positions"""
        created = []
        for i in xrange(int(cellmap.size[0]*cellmap.size[1]*cls.PER_TILE)):
            attempt = (random.randint(0, cellmap.size[0]-1),
                       random.randint(0, cellmap.size[1]-1))
            created.append(cls(attempt, cellmap))
        return created

    def sprite(self, player):
        isvisible = False
        tileoffset = [-1 if axis == 1 else 0 for axis in self.direction]
        for tile in [(0,0), (0,1), (1,0), (1,1)]:
            tile = coords.modsum(tile, tileoffset, self.cellmap.size)
            if coords.sum(self.position, tile) in player.visibletiles:
                isvisible = True
                break
        if isvisible:
            return self._pokedsprite(images.DragonRed[self.direction],
                                     layer=20,
                                     offset=coords.mul(tileoffset, images.TILESIZE))

        else:
            return None
