import images

class Dragon:

    def __init__(self, position, string):
        '''Create new sign in position'''
        self.position = position
        self.hunting = False
        self.string = string
        self.message = [None, 0]

    def update(self, playerpos, cellmap):
        '''DOCSTRING NEEDED HERE'''
        if position = playerpos:
            self.suggestmessage(self.string, 50)

    def sprite(self):
        return images.BearRight if self.direction > 0 else images.BearLeft

    def suggestmessage(self, string, priority):
        if priority > self.message[1]:
            self.message = [string, priority]

    def mdnotify(self):
        self.message = [None, 0]