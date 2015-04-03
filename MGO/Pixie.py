import images
import coords
import random
import BaseMGO

class Pixie(BaseMGO.GEMGO):
    """Pixie that says things when walked to"""
    def __init__(self, phrasebook, position, cellmap):
        """Create new pixie in position"""
        super(Pixie, self).__init__(position, cellmap)
        self.direction = -1 # Left
        self.phrasebook = phrasebook
        self.visible = False

    @classmethod
    def place(cls, cellmap):
        """Populate the world with pixies"""
        created = []
        if 'pixies' in cellmap.gemgodefs:
            for pixiedef in cellmap.gemgodefs['pixies']:
                created.append(cls(pixiedef[1], pixiedef[0], cellmap))
        return created

    def update(self, world):
        """Move; tell player if becoming visible"""
        self.move()
        nearbytiles = coords.neighbours(self.position) + [self.position]
        for player in world.players:
            if player.position in nearbytiles:
                phrase = self.phrasebook[random.randint(0, len(self.phrasebook)-1)]
                self._suggestmessage("Pixie: " + phrase, 50)
            if self.position in player.visibletiles:
                if not self.visible:
                    self._suggestmessage("You see a pixie in the distance", 1)
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
        """Sprite facing in random direction (ugly)"""
        if self.position in player.visibletiles:
            image = random.choice([images.PixieLeft, images.PixieRight])
            return self._pokedsprite(image)

        else:
            return None
