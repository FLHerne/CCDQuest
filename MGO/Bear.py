import random
import images
import coords
import config
import pathfind
import terrain
import BaseMGO

class Bear(BaseMGO.GEMGO):
    """Harmless animal that follows the player"""
    PER_TILE = 1/config.get('fauna', 'tiles_per_bear', float, 2500)

    def __init__(self, position, cellmap):
        """Create bear at position"""
        super(Bear, self).__init__(position, cellmap)
        self.direction = -1 # Left
        self.speed = 0.7    # Chance of moving per turn, max 1, min 0
        self.pfmapsize = 16
        self.detectionrange = 16
        self.maxcost = 32   # Max path cost before giving up.
        self.hunting = None

    def directiontoplayer(self, playerpos):
        """Find the best direction to move towards the player"""
        return pathfind.firstmove(self.position, playerpos, Bear.terraincost,
                                  self.cellmap, self.pfmapsize, self.maxcost)

    def update(self, world):
        def chaseplayer(playerpos):
            """Decide whether to chase the player"""
            playerdist = coords.mindist(self.position, playerpos, self.cellmap.size)
            if (sum(ax**2 for ax in playerdist) > self.detectionrange**2):
                # Can't see/smell/hear (?) player
                return False
            if random.random() > self.speed:
                # Bored?
                return False
            return True

        def randommove():
            """Move in random direction"""
            move = [0, random.randint(-1,1)]
            random.shuffle(move)
            return move

        washunting = self.hunting
        self.hunting = None
        for player in world.players:
            if chaseplayer(player.position):
                self.hunting = player
        if self.hunting:
            # Move in direction of player, or randomly if no path found.
            poschange = self.directiontoplayer(self.hunting.position) or randommove()
            if washunting:
                self._suggestmessage("You are being chased by a bear", 1)
            else:
                self._suggestmessage("A bear starts chasing you", 2)
        else:
            # Move randomly.
            poschange = randommove()
            if washunting:
                self._suggestmessage("The bear has lost interest in you", 1)

        self.direction = poschange[0] if abs(poschange[0]) else self.direction
        newpos = coords.modsum(self.position, poschange, self.cellmap.size)

        if not self.cellmap[newpos]['solid']:
            self.position = newpos
        for player in world.players:
            if self.position == player.position:
                player.scattercoins(4, random.randint(4,8))
                self._suggestmessage("The bear rips a hole in your bag!", 6)

    @staticmethod
    def terraincost(cell):
        """Determine cost of a cell for pathfinding"""
        cost = 1.5 if not cell['transparent'] else 1.0
        cost += float(abs(cell['temperature'] - 20)) / 16
        cost += float(cell['sogginess']) / 8
        # Bears are spooked by artificially-smooth surfaces.
        cost += max(0, 5 - cell['roughness'])
        return cost

    @classmethod
    def place(cls, cellmap):
        """Create bears in random positions, favouring suitable terrain types"""
        typecosts = [cls.terraincost(t) for t in terrain.types]
        mintc, maxtc = min(typecosts), max(typecosts)
        def normterraincost(cell):
            return (cls.terraincost(cell) - mintc) / (maxtc - mintc)
        created = []
        numtocreate = int(cellmap.size[0]*cellmap.size[1]*cls.PER_TILE)
        for i in xrange(numtocreate * 20): # Avoid infinite loop if not placeable.
            attempt = (random.randint(0, cellmap.size[0]-1),
                       random.randint(0, cellmap.size[1]-1))
            cell = cellmap[attempt]
            if cell['solid'] or cell['sogginess'] > 90:
                continue
            if random.random() > normterraincost(cell):
                created.append(cls(attempt, cellmap))
        return created

    def sprite(self, player):
        if self.position in player.visibletiles:
            image = images.BearRight if self.direction > 0 else images.BearLeft
            return self._pokedsprite(image, layer=1)
        else:
            return None
