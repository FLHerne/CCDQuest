import random
import images

class BaseMGO(object):
    def __init__(self):
        self.message = (None, 0)

    def _suggestmessage(self, string, priority):
        if priority > self.message[1]:
            self.message = [string, priority]

    def mdnotify(self):
        self.message = [None, 0]

class GEMGO(BaseMGO):
    def __init__(self, position, cellmap):
        super(GEMGO, self).__init__()
        self.position = tuple(position)
        self.cellmap = cellmap

    @classmethod
    def place(cls, cellmap):
        """Create set of objects with random positions"""
        created = []
        for i in xrange(int(cellmap.size[0]*cellmap.size[1]*cls.PER_TILE)):
            attempt = (random.randint(0, cellmap.size[0]-1),
                       random.randint(0, cellmap.size[1]-1))
            created.append(cls(attempt, cellmap))
        return created

    def update(self, world):
        pass

    def sprite(self, player):
        return None

    def _pokedsprite(self, image, layer=-1, offset=(0,0)):
        """Return a sprite, calculating coord from gemgo position and image size"""
        return (image,
                (self.position[0]*images.TILESIZE + (images.TILESIZE-image.get_width())/2 + offset[0],
                 self.position[1]*images.TILESIZE + (images.TILESIZE-image.get_height())/2 + offset[1]),
                layer)
