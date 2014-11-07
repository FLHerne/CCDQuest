import images
import coords
import random
import MGO

class Pixie(MGO.GEMGO):
    '''Pixie that says things when walked to'''
    def __init__(self, phrasebook, position, cellmap):
        '''Create new pixie in position'''
        super(Pixie, self).__init__(position, cellmap)
        self.direction = -1 # Left
        self.phrasebook = phrasebook
        self.visible = False

    @classmethod
    def place(cls, cellmap):
        created = []
        for pixiedef in cellmap.pixiedefs:
            created.append(cls(pixiedef[1], pixiedef[0], cellmap))
        return created

    def update(self, player):
        '''DOCSTRING NEEDED HERE'''
        self.move()
        ppx, ppy = player.position
        for testx in (ppx-1, ppx, ppx+1):
            for testy in (ppy-1, ppy, ppy+1):
                if self.position == (testx, testy):
                    phrase = self.phrasebook[random.randint(0, len(self.phrasebook)-1)]
                    self._suggestmessage("Pixie: " + phrase, 50)

        if self.position in player.visibletiles:
            if not self.visible:
                self._suggestmessage("You see a pixie in the distance", 1)
            self.visible = True
        else:
            self.visible = True

    def move(self):

        def randommove():
            '''Move in random direction'''
            move = [0, random.randint(-1,1)]
            random.shuffle(move)
            return move

        poschange = randommove()

        self.direction = poschange[0] if abs(poschange[0]) else self.direction
        newpos = coords.mod(coords.sum(self.position, poschange), self.cellmap.size)

        if self.cellmap[newpos]['solid']:
            return False
        self.position = newpos
        return True

    def sprite(self, player):
        if self.position in player.visibletiles:
            if random.getrandbits(1):
                return images.PixieLeft, self._pixelpos(), -1
            else:
                return images.PixieRight, self._pixelpos(), -1

        else:
            return None



