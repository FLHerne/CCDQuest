from colors import *
import collectables
import images

class Cell:
    '''A single square in the world grid, with many properties'''
    DAMAGEDCOST = 5
    BURNINGCOST = 200
    def __init__(self, groundcolor, collectablecolor):
        '''Set up initial attributes'''
        self.damaged = False
        self.burning = False
        self.explored = False
        self.visible = False
        self.name = "UNNAMED TERRAIN"
        self.collectableitem = None
        self.top = False
        self.destructable = True
        self.temperature = 20
        self.fireignitechance = 0
        self.fireoutchance = 1
        self.hasroof = False
        if groundcolor == BLACK:
            self.image = images.Wall
            self.transparent = False
            self.solid = True
            self.difficulty = 3
        elif groundcolor == GREY:
            self.image = images.Rock
            self.transparent = True
            self.solid = False
            self.difficulty = 5
            self.name = "rocky ground"
        elif groundcolor == BROWN:
            self.image = images.Wood
            self.transparent = True
            self.solid = False
            self.difficulty = 2
            self.name = "wooden planking"
            self.fireignitechance = 0.4
            self.fireoutchance = 0.1
        elif groundcolor == WHITE:
            self.image = images.Snow
            self.transparent = True
            self.solid = False
            self.difficulty = 4
            self.name = "snow"
            self.temperature = -5
        elif groundcolor == LIGHTBLUE:
            self.image = images.Water
            self.transparent = True
            self.solid = False
            self.difficulty = 25
            self.name = "water"
            self.destructable = False
            self.temperature = 12
        elif groundcolor == BLUE:
            self.image = images.DeepWater
            self.transparent = True
            self.solid = True
            self.difficulty = 25
            self.name = "deep water"
            self.destructable = False
            self.temperature = 8
        elif groundcolor == GREEN:
            self.image = images.Grass
            self.transparent = True
            self.solid = False
            self.difficulty = 2
            self.name = "grass"
            self.fireignitechance = 0.1
            self.fireoutchance = 0.3
        elif groundcolor == BLUEGREY:
            self.image = images.Marsh
            self.transparent = True
            self.solid = False
            self.difficulty = 20
            self.name = "marshland"
        elif groundcolor == CYAN:
            self.image = images.Glass
            self.transparent = True
            self.solid = True
            self.difficulty = 3
            self.name = "window"
        elif groundcolor == DARKGREEN:
            self.image = images.Trees
            self.transparent = False
            self.solid = False
            self.difficulty = 8
            self.name = "forest"
            self.fireignitechance = 0.5
            self.fireoutchance = 0.1
            self.top = True
        elif groundcolor == DARKYELLOW:
            self.image = images.Sand
            self.transparent = True
            self.solid = False
            self.difficulty = 3
            self.name = "sand"
        elif groundcolor == LIGHTYELLOW:
            self.image = images.Paving
            self.transparent = True
            self.solid = False
            self.difficulty = 1
            self.name = "paving"
        elif groundcolor == DARKPINK:
            self.image = images.Floor
            self.transparent = True
            self.solid = False
            self.difficulty = 1
            self.name = "floor"
            self.fireignitechance = 0.5
            self.fireoutchance = 0.02
            self.hasroof = True
        else:
            raise Exception("Unknown map color")

        if collectablecolor == YELLOW:
            self.collectableitem = collectables.COIN
        elif collectablecolor == BROWN:
            self.collectableitem = collectables.CHOCOLATE
        elif collectablecolor == RED:
            self.collectableitem = collectables.DYNAMITE

    def draw(self, drawSurface, x, y):
        '''Blit cell graphics to the specified surface'''
        DrawPos = (x*images.TILESIZE, y*images.TILESIZE)
        if not self.explored:
            drawSurface.blit(images.Unknown, DrawPos)
            return
        drawSurface.blit(self.image, DrawPos)
        if self.damaged:
            drawSurface.blit(images.Damaged, DrawPos)
        if self.collectableitem != None:
            drawSurface.blit(images.Collectables[self.collectableitem], DrawPos)
        if self.burning:
            drawSurface.blit(images.Burning, DrawPos)
        if not self.visible:
            drawSurface.blit(images.NonVisible, DrawPos)

    def destroy(self):
        '''Change cell attributes to reflect destruction'''
        if not self.destructable:
            return False
        self.damaged = True
        self.hasroof = False
        self.name = "shattered debris"
        self.collectableitem = None
        self.top = False
        self.fireignitechance = 0
        self.fireoutchance = 1
        self.transparent = True
        self.solid = False
        self.difficulty += Cell.DAMAGEDCOST
        return True
