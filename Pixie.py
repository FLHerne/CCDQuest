import images
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

    def update(self, playerpos):
        '''DOCSTRING NEEDED HERE'''
        self.move(playerpos, self.cellmap)
        ppx = playerpos[0]
        ppy = playerpos[1]
        for testx in (ppx-1, ppx, ppx+1):
            for testy in (ppy-1, ppy, ppy+1):
                if self.position == (testx, testy):
                    phrase = self.phrasebook[random.randint(0, len(self.phrasebook)-1)]
                    self._suggestmessage("Pixie: " + phrase, 50)

        if self.cellmap[self.position]['visible']:
            if not self.visible:
                self._suggestmessage("You see a pixie in the distance", 1)
            self.visible = True
        else:
            self.visible = True

    def move(self, playerpos, cellmap):

        def randommove():
            '''Move in random direction'''
            move = [0, random.randint(-1,1)]
            random.shuffle(move)
            return move

        poschange = randommove()

        self.direction = poschange[0] if abs(poschange[0]) else self.direction
        newpos = ((self.position[0]+poschange[0]) % cellmap.size[0],
                  (self.position[1]+poschange[1]) % cellmap.size[1])

        if cellmap[newpos]['solid']:
            return False
        self.position = newpos
        return True

    def sprite(self):
        if self.cellmap[self.position]['visible']:
            return images.Pixie, self._pixelpos(), -1
        else:
            return None



