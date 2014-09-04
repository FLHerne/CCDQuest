import images
from colours import *

class Cell:
    '''A single square in the world grid, with many properties'''
    COIN = 1
    CHOCOLATE = 2
    DYNAMITE = 3
    def __init__(self, image, trans, solid, difficulty, name = "UNNAMED TERRAIN", collectableItem = None, top = False, destructable = True, temperature = 20):
        '''Set up initial attributes'''
        self.image = image
        self.transparent = trans
        self.solid = solid
        self.difficulty = difficulty
        self.damaged = False
        self.explored = False
        self.visible = False
        self.collectableItem = collectableItem
        self.top = top
        self.destructable = destructable
        self.name = name
        self.temperature = temperature
    def draw(self, drawSurface, x, y):
        '''Blit cell graphics to the specified surface'''
        DrawPos = (x*images.BLOCKSIZE, y*images.BLOCKSIZE)
        if not self.explored:
            drawSurface.blit(images.Unknown, DrawPos)
            return
        drawSurface.blit(self.image, DrawPos)
        if self.damaged:
            drawSurface.blit(images.Damage, DrawPos)
        if self.collectableItem != None:
            drawSurface.blit(images.CollectablesImages[self.collectableItem], DrawPos)
        if not self.visible:
            drawSurface.blit(images.NonVisible, DrawPos)

DEEPWATER = Cell(images.DeepWater, True, True, 25, "deep water", destructable = False, temperature=8)
GLASS = Cell(images.Glass, True, True, 3, "window")
GRASS = Cell(images.Grass, True, False, 2, "turf")
ROCK = Cell(images.Rock, True, False, 5, "rocky ground")
SAND = Cell(images.Sand, True, False, 3, "sand")
SNOW = Cell(images.Snow, True, False, 4, "snow", temperature= -5)
SPACE = Cell(images.Space, True, False, 1, "paving")
TREES = Cell(images.Trees, False, False, 8, "forrest", top=True)
WALL = Cell(images.Wall, False, True, 3)
UKWALL = Cell(images.Unknown, False, True, 3)
WATER = Cell(images.Water, True, False, 25, "water", destructable=False, temperature=12)
MARSH = Cell(images.Marsh, True, False, 20, "marshland")
WOOD = Cell(images.Wood, True, False, 2, "wooden planking")

def UnMapGroundColour(colour):
    '''take colours from the ground image, and return the appropriate predefined cell'''
    if colour == BLACK:
        return WALL
    elif colour == GREY:
        return ROCK
    elif colour == BROWN:
        return WOOD
    elif colour == WHITE:
        return SNOW
    elif colour == LIGHTBLUE:
        return WATER
    elif colour == BLUE:
        return DEEPWATER    
    elif colour == GREEN:
        return GRASS
    elif colour == BLUEGREY:
        return MARSH
    elif colour == CYAN:
        return GLASS
    elif colour == DARKGREEN:
        return TREES
    elif colour == DARKYELLOW:
        return SAND
    else:
        return SPACE

def UnMapCollectablesColour(colour):
    '''take colours from the collectables image, and set cell properties'''
    if colour == YELLOW:
        return Cell.COIN
    elif colour == BROWN:
        return Cell.CHOCOLATE
    elif colour == RED:
        return Cell.DYNAMITE
    else:
        return None

