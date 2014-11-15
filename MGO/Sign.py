import images
import BaseMGO

class Sign(BaseMGO.GEMGO):
    """Sign that displays message when walked over"""
    def __init__(self, string, position, cellmap):
        """Create new sign in position"""
        super(Sign, self).__init__(position, cellmap)
        self.string = string
        self.visible = False

    @classmethod
    def place(cls, cellmap):
        created = []
        if 'signs' in cellmap.gemgodefs:
            for signdef in cellmap.gemgodefs['signs']:
                created.append(cls(signdef[1], signdef[0], cellmap))
        return created

    def update(self, world):
        """Display message if becoming visible or trodden on"""
        for player in world.players:
            if player.position == self.position:
                self._suggestmessage("The sign reads: " + self.string, 50)
            if self.position in player.visibletiles:
                if not self.visible:
                    self._suggestmessage("You see a sign in the distance", 1)
                self.visible = True
            else:
                self.visible = False

    def sprite(self, player):
        if self.cellmap[self.position]['explored']:
            return images.Sign, self._pixelpos(), -1
        else:
            return None
