class MGO(object):
    def __init__(self):
        self.message = (None, 0)

    def _suggestmessage(self, string, priority):
        if priority > self.message[1]:
            self.message = [string, priority]

    def mdnotify(self):
        self.message = [None, 0]

class GEMGO(MGO):
    def __init__(self, position, cellmap):
        super(GEMGO, self).__init__()
        self.position = list(position)
        self.cellmap = cellmap


    def update(self, playerpos, cellmap):
        pass


    def sprite(self):
        pass
