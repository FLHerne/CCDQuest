import images
import BaseMGO

class Portal(BaseMGO.GEMGO):
    """Sign that displays message when walked over"""
    def __init__(self, position, cellmap):
        """Create new sign in position"""
        super(Portal, self).__init__(position, cellmap)

    @classmethod
    def place(cls, cellmap):
        created = []
        if 'portals' in cellmap.gemgodefs:
            for portaldef in cellmap.gemgodefs['portals']:
                created.append(cls(portaldef[0], cellmap))
        return created

    def update(self, player):
        """Display message if becoming visible or trodden on"""
        if self.position == player.position:
            self._suggestmessage("Fizzap!", 50)

    def sprite(self, player):
        if self.cellmap[self.position]['explored']:
            return images.Portal, self._pixelpos(), -1
        else:
            return None
