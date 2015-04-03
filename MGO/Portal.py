import images
import BaseMGO

class Portal(BaseMGO.GEMGO):
    """Portals teleport the player to other locations/worlds"""
    def __init__(self, position, destination, localin, remotein, cellmap):
        """
        Create new portal
        position, destination: obvious
        local/remotein: Is destination of >0 portals in this/other world(s)
        """
        super(Portal, self).__init__(position, cellmap)
        self.destination = destination
        if destination is None:
            outindex = 0
        elif destination[0] == cellmap.mapdef['dir']:
            outindex = 1
        else:
            outindex = 2
        inindex = localin + 2*remotein
        self.image = images.Portal[outindex][inindex]

    @classmethod
    def place(cls, cellmap):
        """Place portals when creating world"""
        created = []
        if 'portals' in cellmap.gemgodefs:
            for portaldef in cellmap.gemgodefs['portals']:
                created.append(cls(*(portaldef + (cellmap,))))
        return created

    def update(self, world):
        """Teleport player when trodden on"""
        for player in world.players:
            if (player.position == self.position) and self.destination:
                self._suggestmessage("Fizzap!", 50)
                player.delayedteleport(*self.destination)

    def sprite(self, player):
        """Sprite depends on incoming and outgoing links"""
        if self.cellmap[self.position]['explored']:
            return self._pokedsprite(self.image, layer=-2)
        else:
            return None
