import images
import random

class Pixie:
    '''Pixie that says things when walked to'''
    def __init__(self, position, phrase):
        '''Create new pixie in position'''
        self.position = position
        self.direction = -1 # Left
        self.phrase = phrase
        self.message = [None, 0]
        self.visible = False
        print "pixie inited"

    def update(self, playerpos, cellmap):
        '''DOCSTRING NEEDED HERE'''
        self.move(playerpos, cellmap)
        ppx = playerpos[0]
        ppy = playerpos[1]
        for testx in (ppx-1, ppx, ppx+1):
            for testy in (ppy-1, ppy, ppy+1):
                if self.position == (testx, testy):
                    self.suggestmessage("The pixie says: " + self.phrase, 50)
                    print "pixiemessage triggered"

        if cellmap[self.position]['visible']:
            if not self.visible:
                self.suggestmessage("You see a pixie in the distance", 1)
                print "pixie seen"
            self.visible = True
        else:
            self.visible = True

    def move(self, playerpos, cellmap):

        def randommove():
            '''Move in random direction'''
            move = [0, random.randint(-1,1)]
            random.shuffle(move)
            return move

        print "pixie moved"
        poschange = randommove()

        self.direction = poschange[0] if abs(poschange[0]) else self.direction
        newpos = ((self.position[0]+poschange[0]) % cellmap.size[0],
                  (self.position[1]+poschange[1]) % cellmap.size[1])

        if cellmap[newpos]['solid']:
            return False
        self.position = newpos
        return True

    def sprite(self):
        return images.Pixie

    def suggestmessage(self, string, priority):
        if priority > self.message[1]:
            self.message = [string, priority]

    def mdnotify(self):
        self.message = [None, 0]
