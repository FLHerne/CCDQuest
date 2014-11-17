import images
import BaseMGO

class Portal(BaseMGO.GEMGO):
    """Sign that displays message when walked over"""
    def __init__(self, position, destination, cellmap):
        """Create new sign in position"""
        super(Portal, self).__init__(position, cellmap)
        self.destination = destination

    @classmethod
    def place(cls, cellmap):
        created = []
        if 'portals' in cellmap.gemgodefs:
            for portaldef in cellmap.gemgodefs['portals']:
                created.append(cls(portaldef[0], portaldef[1:3], cellmap))
        return created

    def update(self, world):
        """Display message if becoming visible or trodden on"""
        for player in world.players:
            if player.position == self.position:
                self._suggestmessage("Fizzap!", 50)
                player.delayedteleport(*self.destination)

    def sprite(self, player):
        if self.cellmap[self.position]['explored']:
            return images.Portal, self._pixelpos(), -1
        else:
            return None
