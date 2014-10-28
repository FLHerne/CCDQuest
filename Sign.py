import images

class Sign:
    '''Sign that displays message when walked over'''
    def __init__(self, position, string):
        '''Create new sign in position'''
        self.position = position
        self.string = string
        self.message = [None, 0]
        self.visible = False

    def update(self, playerpos, cellmap):
        '''DOCSTRING NEEDED HERE'''
        if self.position == playerpos:
            self.suggestmessage("The sign reads: " + self.string, 50)

    def sprite(self):
        return images.Sign

    def suggestmessage(self, string, priority):
        if priority > self.message[1]:
            self.message = [string, priority]

    def mdnotify(self):
        self.message = [None, 0]

    def visiblenotify(self, visible):
        if visible and not self.visible:
            self.suggestmessage("You see a sign in the distance", 1)
        self.visible = visible