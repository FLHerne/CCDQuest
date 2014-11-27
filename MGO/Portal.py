import images
import BaseMGO

class Portal(BaseMGO.GEMGO):
    """Sign that displays message when walked over"""
    def __init__(self, position, destination, localin, remotein, cellmap):
        """Create new sign in position"""
        super(Portal, self).__init__(position, cellmap)
        self.destination = destination
        if destination is None:
            outindex = 0
        elif destination[0] == cellmap.mapdef['dir']:
            outindex = 1
        else:
            outindex = 2
        inindex = localin + 2*remotein
        print position, localin, remotein
        self.image = images.Portal[outindex][inindex]

    @classmethod
    def place(cls, cellmap):
        created = []
        if 'portals' in cellmap.gemgodefs:
            for portaldef in cellmap.gemgodefs['portals']:
                created.append(cls(*(portaldef + (cellmap,))))
        return created

    def update(self, world):
        """Display message if becoming visible or trodden on"""
        for player in world.players:
            if (player.position == self.position) and self.destination:
                self._suggestmessage("Fizzap!", 50)
                player.delayedteleport(*self.destination)

    def sprite(self, player):
        if self.cellmap[self.position]['explored']:
            return self.image, self._pixelpos((-6, -6)), -1
        else:
            return None
