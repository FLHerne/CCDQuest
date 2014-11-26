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
                destination = portaldef[1:3] if len(portaldef) >= 3 else None
                created.append(cls(portaldef[0], destination, cellmap))
        return created

    def update(self, world):
        """Display message if becoming visible or trodden on"""
        for player in world.players:
            if (player.position == self.position) and self.destination:
                self._suggestmessage("Fizzap!", 50)
                player.delayedteleport(*self.destination)

    def sprite(self, player):
        if self.cellmap[self.position]['explored']:
            if self.destination is None:
                image = images.Portal[0][1]
            elif self.destination[0] == self.cellmap.mapdef['dir']:
                image = images.Portal[1][0]
            else:
                image = images.Portal[2][0]
            return image, self._pixelpos((-6, -6)), -1
        else:
            return None
