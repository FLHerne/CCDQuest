#!/usr/bin/env python2.6

import pygame
import sys
import time
import TextBox

from colours import *

# -----------------------------------------------------------------------------

printDebug = True
printError = True

def DebugPrint(Message):            # Messages which the end-user need not see, but may be useful to the developer
    if printDebug:
        print(Message)
        
def ErrorPrint(Message):            # Messages which indicate that something has gone wrong
    if printError:
        print(Message)

# -----------------------------------------------------------------------------
        
#groundFile = 'World7-ground.png'				#Image to use as map
#collectablesFile = 'World7-collectables.png'
groundFile = 'map/latestRandomGen.png'                #Image to use as map
collectablesFile = 'map/blank.png'

ground = pygame.image.load(groundFile)
collectables = pygame.image.load(collectablesFile)
worldSize = ground.get_rect().size

worldSize = [worldSize[0], worldSize[1]]               #Size of image - FIXME
BLOCKSIZE = 8                       #Size of each square in the grid
VISIBILITY = 15                     #How far can you see in an approximate circle
HUDFONTSIZE = 20                    # Score counter etc
totalCoins = 0                      #How many coins are there in total? (initialise)
windowSize = (740, 480)
viewBlocks = (int((windowSize[0]-100)/BLOCKSIZE), int(windowSize[1]/BLOCKSIZE))

scores = {"coins" : 0,
    "chocolate" : 10000, 
    "dynamite" : 15}

animCounter = 0
animLength = 36

window = pygame.display.set_mode(windowSize)

# -----------------------------------------------------------------------------

pygame.key.set_repeat(100, 75)      # press-and hold for faster movement
USEARROWS = True                    # set the keyboard controlls mode

if USEARROWS:                       # mode using arrow keys
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    BLAST = pygame.K_SPACE
else:                               # mode using WASD
    UP = pygame.K_w
    DOWN = pygame.K_s
    LEFT = pygame.K_a
    RIGHT = pygame.K_d
    BLAST = pygame.K_SPACE

# -----------------------------------------------------------------------------

UnknownImage = pygame.image.load("tiles/Unknown.png")           # Used for tiles that must appear to be empty blank nothingness

DamageImage = pygame.image.load("tiles/Damage.png")             # An overlay for damaged (blown-up) tiles
DamageImage = DamageImage.convert_alpha()                       # this image is transparent, so the alpha must be used too

CoinImage = pygame.image.load("tiles/Coin.png")                 # images for collectables
CoinImage = CoinImage.convert_alpha()                           # collectables have transparent backgrounds
ChocImage = pygame.image.load("tiles/Chocolate.png")
ChocImage = ChocImage.convert_alpha()
DynamiteImage = pygame.image.load("tiles/Dynamite.png")
DynamiteImage = DynamiteImage.convert_alpha()

WaterImage = pygame.image.load("tiles/Water.png")               # images for terrain
DeepWaterImage = pygame.image.load("tiles/DeepWater.png")
RockImage = pygame.image.load("tiles/Rock.png")
SpaceImage = pygame.image.load("tiles/Floor.png")
GrassImage = pygame.image.load("tiles/Grass.png")
MarshImage = pygame.image.load("tiles/Marsh.png")
WallImage = pygame.image.load("tiles/Wall.png")
GlassImage = pygame.image.load("tiles/Glass.png")
WoodImage = pygame.image.load("tiles/Wood.png")
TreesImage = pygame.image.load("tiles/Trees.png")
SandImage = pygame.image.load("tiles/Sand.png")
SnowImage = pygame.image.load("tiles/Snow.png")

collectablesImages = { 1 : CoinImage,                           # semi-enum for referencing collectable images
                       2 : ChocImage,
                       3 : DynamiteImage}
                        
class Cell:
    COIN = 1
    CHOCOLATE = 2
    DYNAMITE = 3
    def __init__(self, image, trans, solid, difficulty, reDraw = False, collectableItem = None, top = False, destructable = True):
        self.image = image
        self.transparent = trans
        self.solid = solid
        self.difficulty = difficulty
        self.damaged = False
        self.alwaysRedraw = reDraw
        self.collectableItem = collectableItem
        self.top = top
        self.destructable = destructable
    def draw(self, drawSurface, x, y):
        drawSurface.blit(self.image, (x, y))
        if self.damaged:
            drawSurface.blit(DamageImage, (x, y))
        if self.collectableItem != None:
            drawSurface.blit(collectablesImages[self.collectableItem], (x, y))
                   
DEEPWATER = Cell(DeepWaterImage, True, True, 25, True, destructable = False)
GLASS = Cell(GlassImage, True, True, 3)
GRASS = Cell(GrassImage, True, False, 2)
ROCK = Cell(RockImage, True, False, 5)
SAND = Cell(SandImage, True, False, 3)
SNOW = Cell(SnowImage, True, False, 4)
SPACE = Cell(SpaceImage, True, False, 1)
TREES = Cell(TreesImage, False, False, 8, False, None, True)
UNKNOWN = Cell(UnknownImage, True, True, 3)
WALL = Cell(WallImage, False, True, 3)
UKWALL = Cell(UnknownImage, False, True, 3)
WATER = Cell(WaterImage, True, False, 25, True, None, False, False)
MARSH = Cell(MarshImage, True, False, 20, True)
WOOD = Cell(WoodImage, True, False, 2)

# -----------------------------------------------------------------------------
  
PLAYER1 = MAGENTA 
START = MAGENTA

HudImage = pygame.image.load("HudPanel.png")
HudImage = HudImage.convert_alpha()

# -----------------------------------------------------------------------------

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
        
class StartPosUndefined(Exception):
    pass

# -----------------------------------------------------------------------------

RealMap = {}
for x in range(1-VISIBILITY, worldSize[0]+1+VISIBILITY):	#Make the edge of the world a wall
    for y in range(1-VISIBILITY, worldSize[1]+1+VISIBILITY):
        RealMap[x, y] = WALL


groundMap = pygame.PixelArray(ground)
collectablesMap = pygame.PixelArray(collectables)

for x in range(1, worldSize[0]+1):
    for y in range(1, worldSize[1]+1):
        groundColour = ground.unmap_rgb(groundMap[x-1,y-1])
        RealMap[x, y] = UnMapGroundColour(groundColour)
        collectableColour = collectables.unmap_rgb(collectablesMap[x-1,y-1])
        RealMap[x, y] = Cell(RealMap[x, y].image,
                             RealMap[x, y].transparent,
                             RealMap[x, y].solid,
                             RealMap[x, y].difficulty,
                             RealMap[x, y].alwaysRedraw,
                             UnMapCollectablesColour(collectableColour),
                             RealMap[x, y].top,
                             RealMap[x, y].destructable
                             )
            
        if RealMap[x, y].collectableItem == Cell.COIN:
            totalCoins += 1
        if collectableColour == START:
            DebugPrint("Found starting position")
            Pos = [x, y]
if Pos is None:
    raise StartPosUndefined()

for x in (1, worldSize[0]+1):
    for y in range(1, worldSize[1]+1):
        RealMap[x, y] = UKWALL
for x in range(1, worldSize[0]+1):
    for y in (1, worldSize[1]+1):
        RealMap[x, y] = UKWALL
    
del groundMap
del collectablesMap

# -----------------------------------------------------------------------------

Map = {}						#Initialise visible map with unknowness
for x in range(1-VISIBILITY, worldSize[0]+1+VISIBILITY):
    for y in range(1-VISIBILITY, worldSize[1]+1+VISIBILITY):
        Map[x, y] = UNKNOWN
        
# -----------------------------------------------------------------------------
        
window.fill(GREY)

# -----------------------------------------------------------------------------

def DiagonalCheck():
    '''Test visibility along (offset) diagronals away from player'''
    x = Pos[0]
    y = Pos[1]
    Map[x, y] = RealMap[x, y]                       # make the currently occupied cell visible
    for horizontal in (True, False):                # horizontal and vertical
        for Dir1 in (-1, 1):                        # left/right or up/down
            for Dir2 in (-1, 1):                    # final division into octants
                Base = 0                            # how far horizontally or vertically the test ray is from the player
                while (abs(Base) < VISIBILITY and
                    RealMap[Pos[0]+(Base if horizontal else 0),
                        Pos[1]+(0 if horizontal else Base)].transparent):   # repeatedly test if a cell is transparent and within a bounding square
                    Base += Dir1
                    if horizontal:
                        x = Pos[0] + Base
                        y = Pos[1]
                    else:
                        x = Pos[0]
                        y = Pos[1] + Base
                    Map[x, y] = RealMap[x, y]
                    while RealMap[x, y].transparent and ((Pos[1]-y)**2) + ((Pos[0]-x)**2) <= VISIBILITY**2: # test in bounding circle
                        if horizontal:                                                                      # move diagonally
                            x += Dir1
                            y += Dir2
                        else:
                            x += Dir2
                            y += Dir1
                        Map[x, y] = RealMap[x, y]                                                           # make visible
                    Map[x, y] = RealMap[x, y]                                                               # make the first opaque cell visible too
                    #Base += Dir1		#FIXME - either the main diagonals aren't shown, or the ends of the cross aren't
                Map[x, y] = RealMap[x, y]
                
# -----------------------------------------------------------------------------

def CrossCheck():
    '''Check visibility straight up, down, left and right'''
    for i in (-1, 1):                                                           # Horizontally left and right
        X = 0                                                                   # start at the player      
        while RealMap[(X*i)+Pos[0], Pos[1]].transparent and X < VISIBILITY:     # if transparent and within bounding range
            Map[(X*i)+Pos[0], Pos[1]] = RealMap[(X*i)+Pos[0], Pos[1]]           # make visible
            X += 1                                                              # move away from player
        Map[(X*i)+Pos[0], Pos[1]] = RealMap[(X*i)+Pos[0], Pos[1]]               # make final cell visible
    for i in (-1, 1):                                                           # Repeat as above, but vertically
        Y = 0
        while RealMap[Pos[0], (Y*i)+Pos[1]].transparent and Y < VISIBILITY:
            Map[Pos[0], (Y*i)+Pos[1]] = RealMap[Pos[0], (Y*i)+Pos[1]]
            Y += 1
        Map[Pos[0], (Y*i)+Pos[1]] = RealMap[Pos[0], (Y*i)+Pos[1]]

        
def ExplosionValid(x, y, Dynamite):
    '''test if an explosion is currently possible'''
    if (Dynamite > 0 and RealMap[x, y].destructable):
        DebugPrint("Explosion possible")
    else:
        DebugPrint("Explosion not possible")
    return (Dynamite > 0 and RealMap[x, y].destructable)
        
        
def Explosion(Dynamite, Centrex, Centrey):
    '''Clear a 3x3 square using a stick of dynamite'''
    #RealMap[Centrex, Centrey] = SPACE
    DebugPrint("Explosion at " + str(Centrex) + ", " + str(Centrey))
    for x in (-1, 0, 1):                                                        # explosion forms a 3x3 square
        for y in (-1, 0, 1):
            if RealMap[Centrex+x, Centrey+y].collectableItem == Cell.DYNAMITE:
                Explosion(1, Centrex+x, Centrey+y)                              # dynamite sets off neighbouring dynamite
            if RealMap[Centrex+x, Centrey+y].destructable:
                RealMap[Centrex+x, Centrey+y] = Cell(RealMap[Centrex+x, Centrey+y].image, True, False, 4)
                RealMap[Centrex+x, Centrey+y].damaged = True
                RealMap[Centrex+x, Centrey+y].collectableItem = None
                if RealMap[Centrex+x, Centrey+y].image == WoodImage:
                    RealMap[Centrex+x, Centrey+y].image = WaterImage

            
    Dynamite -= 1
    return Dynamite
    
    
def CollectItems(scores):
    '''deal with any colllectables found on the current cell'''
    if RealMap[Pos[0], Pos[1]].collectableItem == Cell.COIN:    #Have we just walked into a coin
        scores["coins"] += 1                                    #Increment score counter
        RealMap[Pos[0], Pos[1]].collectableItem = None	        #Remove coin
        DebugPrint("Collected a coin")
    if RealMap[Pos[0], Pos[1]].collectableItem == Cell.DYNAMITE:
        scores["dynamite"] += 1
        RealMap[Pos[0], Pos[1]].collectableItem = None
        DebugPrint("Collected a stick of dynamite")
    if RealMap[Pos[0], Pos[1]].collectableItem == Cell.CHOCOLATE:
        scores["chocolate"] += 50
        RealMap[Pos[0], Pos[1]].collectableItem = None
        DebugPrint("Collected a bar of chocolate")
    return scores

        
def HandleEvents(scores):
    '''respond to user input'''
    quitting = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitting = True
        if event.type == pygame.KEYDOWN:
            if event.key == UP:
                if not RealMap[Pos[0], Pos[1]-1].solid:	#We haven't collided with anthing
                    Pos[1] -= 1
            if event.key == DOWN:
                if not RealMap[Pos[0], Pos[1]+1].solid:
                    Pos[1] += 1
            if event.key == LEFT:
                if not RealMap[Pos[0]-1, Pos[1]].solid:
                    Pos[0] -= 1
            if event.key == RIGHT:
                if not RealMap[Pos[0]+1, Pos[1]].solid:
                    Pos[0] += 1
            if event.key == BLAST and ExplosionValid(Pos[0], Pos[1], scores["dynamite"]):
                scores["dynamite"] = Explosion(scores["dynamite"], Pos[0], Pos[1])
            if scores["chocolate"] >= 0:
                scores["chocolate"] -= Map[Pos[0], Pos[1]].difficulty
            else:
                quitting = True
    scores = CollectItems(scores)
    return quitting, scores
    
    
def UpdateVisible():
    '''copy parts of of RealMap into map, as appropriate'''
    #CrossCheck()
    DiagonalCheck()

    
#def TestNeighbours(x, y, centreTileType):
#	if (RealMap[x, y+1] != centreTileType) and RealMap[x+1, y] != centreTileType:
#		return 
    
    
def DrawTiles():
    tlX = int(Pos[0]-viewBlocks[0]/2)
    tlY = int(Pos[1]-viewBlocks[1]/2)
    for x in range(0, viewBlocks[0]):
        for y in range(0, viewBlocks[1]):
            Map[tlX+x, tlY+y].draw(window, x*BLOCKSIZE, y*BLOCKSIZE)

def DrawPlayer():
    '''draw the player as a blinking circle'''
    if (animCounter%9 != 0) and (Map[Pos[0], Pos[1]].top == False):
        pygame.draw.circle(window, PLAYER1, (viewBlocks[0]/2*BLOCKSIZE+BLOCKSIZE/2, viewBlocks[1]/2*BLOCKSIZE+BLOCKSIZE/2), int(BLOCKSIZE/2))


def DrawHud(scores, drawSurface):
    '''Draw the heads-up display, with current information'''
    #pygame.draw.rect(drawSurface, BLACK, (windowSize[0]-100, 0, 100, windowSize[1]))
    drawSurface.blit(HudImage, (windowSize[0]-100, 0, 100, windowSize[1]))
    TextBox.Print(drawSurface,
                  False,
                  windowSize[0]-95, 75,
                  100,
                  None,
                  BLACK,
                  'Arial', HUDFONTSIZE,
                  str(scores["coins"]) + "/" + str(totalCoins),
                  True,
                  [False, windowSize[1]])
    TextBox.Print(drawSurface,
                  False,
                  windowSize[0]-95, 275,
                  100,
                  None,
                  BLACK,
                  'Arial', HUDFONTSIZE,
                  str(scores["dynamite"]),
                  True,
                  [False, windowSize[1]])
    if scores["chocolate"] >= 1000:
        ChocAmountString = str(round(scores["chocolate"] / 1000.0, 2)) + "kg"
    else:
        ChocAmountString = str(scores["chocolate"])+"g"
    TextBox.Print(drawSurface,
                  False,
                  windowSize[0]-95, 175,
                  100,
                  None,
                  BLACK,
                  'Arial', HUDFONTSIZE,
                  ChocAmountString,
                  True,
                  [False, windowSize[1]])
    if scores["chocolate"] <= 0:
        TextBox.Print(drawSurface,
                      False,
                      0, 0,
                      windowSize[0],
                      BLACK,
                      WHITE,
                      'Arial', HUDFONTSIZE*2,
                      "You ran out of chocolate!",
                      True,
                      [True, windowSize[1]])
    
    #pygame.transform.scale(world, (90, (world.get_height()/world.get_width())*90), miniWorld)
    #drawSurface.blit(miniWorld, (windowSize[0]-90, 302))
    #miniWorldScale = 90.0/(worldSize[0]*BLOCKSIZE)
    #pygame.draw.rect(drawSurface,
                     #PLAYER1,
                     #((windowSize[0]-90)-(scrollPos[0]*miniWorldScale),
                      #302-               (scrollPos[1]*miniWorldScale),
                      #1+ (windowSize[0]-100)*miniWorldScale,
                      #1+ windowSize[1]*miniWorldScale),
                     #1)


def animCountUpdate(animCounter):
    '''a looping counter for crude animation'''
    if animCounter >= animLength:
        animCounter = 0
    else:
        animCounter += 1
    return animCounter
    
def setup():
    '''to be used at the beginning of the programme'''
    pass

def loop():
    '''to be used repeatedly'''
    pass
  
quitting = False
while not quitting:
    time.sleep(0.04)
    quitting, scores = HandleEvents(scores)
    UpdateVisible()
    DrawTiles()
    DrawPlayer()
    DrawHud(scores, window)
    animCounter = animCountUpdate(animCounter)
    pygame.display.update()
            
pygame.quit()
sys.exit()