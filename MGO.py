import random
import images

class MGO(object):
    def __init__(self):
        self.message = (None, 0)

    def _suggestmessage(self, string, priority):
        if priority > self.message[1]:
            self.message = [string, priority]

    def mdnotify(self):
        self.message = [None, 0]

class GEMGO(MGO):
    PER_TILE = 1/float(1000)
    def __init__(self, position, cellmap):
        super(GEMGO, self).__init__()
        self.position = list(position)
        self.cellmap = cellmap

    @classmethod
    def place(cls, cellmap):
        '''Create set of objects with random positions'''
        created = []
        for i in xrange(int(cellmap.size[0]*cellmap.size[1]*cls.PER_TILE)):
            attempt = (random.randint(0, cellmap.size[0]-1),
                       random.randint(0, cellmap.size[1]-1))
            created.append(cls(attempt, cellmap))
        return created

    def update(self, playerpos, cellmap):
        pass

    def sprite(self):
        return None

    def _pixelpos(self, offset=(0,0)):
        return (self.position[0]*images.TILESIZE + offset[0],
                self.position[1]*images.TILESIZE + offset[1])