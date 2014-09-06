from Map import Map
class World:
    def __init__(self):
        groundfile = 'map/World7-ground.png'
        collectablefile = 'map/World7-collectables.png'
        self.terrain = Map(groundfile, collectablefile)
        
        