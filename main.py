#!/usr/bin/env python2.6

import pygame
import sys
import time
import TextBox

from colours import *

# -----------------------------------------------------------------------------

printDebug = True
printError = True

def DebugPrint(Message):
    if printDebug:
        print(Message)
        
def ErrorPrint(Message):
    if printError:
        print(Message)

# -----------------------------------------------------------------------------
        
#groundFile = 'World7-ground.png'				#Image to use as map
#collectablesFile = 'World7-collectables.png'
groundFile = 'latestRandomGen.png'                #Image to use as map
collectablesFile = 'blank.png'

ground = pygame.image.load(groundFile)
collectables = pygame.image.load(collectablesFile)
worldSize = ground.get_rect().size

worldSize = [worldSize[0], worldSize[1]]               #Size of image - FIXME
BLOCKSIZE = 8                       #Size of each square in the grid
VISIBILITY = 15                      #How far can you see in an approximate circle
HUDFONTSIZE = 20                    # Score counter etc
totalCoins = 0                      #How many coins are there in total? (initialise)
windowSize = (740, 480)

scores = {"coins" : 0,
    "chocolate" : 10000, 
    "dynamite" : 0}

animCounter = 0
animLength = 36

window = pygame.display.set_mode(windowSize)
world = pygame.Surface((worldSize[0]*BLOCKSIZE, worldSize[1]*BLOCKSIZE))

# -----------------------------------------------------------------------------

pygame.key.set_repeat(100, 75)
USEARROWS = True

if USEARROWS:
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    BLAST = pygame.K_SPACE
else:
    UP = pygame.K_w
    DOWN = pygame.K_s
    LEFT = pygame.K_a
    RIGHT = pygame.K_d
    BLAST = pygame.K_SPACE

# -----------------------------------------------------------------------------

UnknownImage = pygame.image.load("Unknown.png")

DamageImage = pygame.image.load("Damage.png")
DamageImage = DamageImage.convert_alpha()

CoinImage = pygame.image.load("Coin.png")
CoinImage = CoinImage.convert_alpha()
ChocImage = pygame.image.load("Chocolate.png")
ChocImage = ChocImage.convert_alpha()
DynamiteImage = pygame.image.load("Dynamite.png")
DynamiteImage = DynamiteImage.convert_alpha()

WaterImage = pygame.image.load("Water.png")
DeepWaterImage = pygame.image.load("DeepWater.png")
RockImage = pygame.image.load("Rock.png")
SpaceImage = pygame.image.load("Floor.png")
GrassImage = pygame.image.load("Grass.png")
MarshImage = pygame.image.load("Marsh.png")
WallImage = pygame.image.load("Wall.png")
GlassImage = pygame.image.load("Glass.png")
WoodImage = pygame.image.load("Wood.png")
TreesImage = pygame.image.load("Trees.png")
SandImage = pygame.image.load("Sand.png")
SnowImage = pygame.image.load("Snow.png")

collectablesImages = { 1 : CoinImage,
                       2 : ChocImage,
                       3 : DynamiteImage}
                        
class Cell:
    COIN = 1
    CHOCOLATE = 2
    DYNAMITE = 3
    def __init__(self, image, trans, solid, difficulty, reDraw = False, collectableItem = None, top = False):
        self.image = image
        self.transparent = trans
        self.solid = solid
        self.difficulty = difficulty
        self.damaged = False
        self.alwaysRedraw = reDraw
        self.collectableItem = collectableItem
        self.top = top
    def draw(self, drawSurface, x, y):
        drawSurface.blit(self.image, ((x*BLOCKSIZE)-BLOCKSIZE, (y*BLOCKSIZE)-BLOCKSIZE))
        if self.damaged:
            drawSurface.blit(DamageImage, ((x*BLOCKSIZE)-BLOCKSIZE, (y*BLOCKSIZE)-BLOCKSIZE))
        if self.collectableItem != None:
            drawSurface.blit(collectablesImages[self.collectableItem], ((x*BLOCKSIZE)-BLOCKSIZE, (y*BLOCKSIZE)-BLOCKSIZE))
                   
DEEPWATER = Cell(DeepWaterImage, True, True, 25, True)
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
WATER = Cell(WaterImage, True, False, 25, True)
MARSH = Cell(MarshImage, True, False, 20, True)
WOOD = Cell(WoodImage, True, False, 2)

# -----------------------------------------------------------------------------
  
PLAYER1 = MAGENTA 
START = MAGENTA

HudImage = pygame.image.load("HudPanel.png")
HudImage = HudImage.convert_alpha()

# -----------------------------------------------------------------------------

def UnMapGroundColour(colour):
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
                             RealMap[x, y].top
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
world.fill(GREY)
miniWorld = pygame.transform.scale(world, (90, (world.get_height()/world.get_width())*90))

# -----------------------------------------------------------------------------

def DiagonalCheck():
    Map[Pos[0], Pos[1]] = RealMap[Pos[0], Pos[1]]
    x = Pos[0]
    y = Pos[1]
    for horizontal in (True, False):
        for Dir1 in (-1, 1):
            for Dir2 in (-1, 1):
                Base = 0
                while (Base < VISIBILITY and
                    RealMap[Pos[0]+(Base if horizontal else 0),
                        Pos[1]+(0 if horizontal else Base)].transparent): 
                    Base += Dir1
                    if horizontal:
                        x = Pos[0] + Base
                        y = Pos[1]
                    else:
                        x = Pos[0]
                        y = Pos[1] + Base
                    Map[x, y] = RealMap[x, y]
                    while RealMap[x, y].transparent and ((Pos[1]-y)**2) + ((Pos[0]-x)**2) <= VISIBILITY**2:
                        if horizontal:
                            x += Dir1
                            y += Dir2
                        else:
                            x += Dir2
                            y += Dir1
                        Map[x, y] = RealMap[x, y]
                    Map[x, y] = RealMap[x, y]
                    #Base += Dir1		#FIXME - either the main diagonals aren't shown, or the ends of the cross aren't
                Map[x, y] = RealMap[x, y]
                
# -----------------------------------------------------------------------------

def CrossCheck():
    '''Check visibility straight up, down, left and right'''
    for i in (-1, 1):				#Horizontal
        X = 0
        while RealMap[(X*i)+Pos[0], Pos[1]].transparent and X < VISIBILITY:
            Map[(X*i)+Pos[0], Pos[1]] = RealMap[(X*i)+Pos[0], Pos[1]]
            X += 1
        Map[(X*i)+Pos[0], Pos[1]] = RealMap[(X*i)+Pos[0], Pos[1]]
    for i in (-1, 1):				#Vertical
        Y = 0
        while RealMap[Pos[0], (Y*i)+Pos[1]].transparent and Y < VISIBILITY:
            Map[Pos[0], (Y*i)+Pos[1]] = RealMap[Pos[0], (Y*i)+Pos[1]]
            Y += 1
        Map[Pos[0], (Y*i)+Pos[1]] = RealMap[Pos[0], (Y*i)+Pos[1]]

        
def ExplosionValid(x, y, Dynamite):
    return (Dynamite > 0 and RealMap[x, y] != WATER and RealMap[x, y] != DEEPWATER)
        
        
def Explosion(Dynamite, Centrex, Centrey):
    '''Clear a 3x3 square using a stick of dynamite'''
    #RealMap[Centrex, Centrey] = SPACE
    DebugPrint("Explosion at " + str(Centrex) + ", " + str(Centrey))
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if RealMap[Centrex+x, Centrey+y].collectableItem == Cell.DYNAMITE:
                Explosion(1, Centrex+x, Centrey+y)
            if RealMap[Centrex+x, Centrey+y] != WATER:
                #RealMap[Centrex+x, Centrey+y] = SPACE
                RealMap[Centrex+x, Centrey+y] = Cell(RealMap[Centrex+x, Centrey+y].image, True, False, 4)
                RealMap[Centrex+x, Centrey+y].damaged = True
                RealMap[Centrex+x, Centrey+y].collectableItem = None
                if RealMap[Centrex+x, Centrey+y].image == WoodImage:
                    RealMap[Centrex+x, Centrey+y].image = WaterImage

            
    Dynamite -= 1
    return Dynamite
    
    
def CollectItems(scores):
        if RealMap[Pos[0], Pos[1]].collectableItem == Cell.COIN:	#Have we just walked into a coin
            scores["coins"] += 1			#Increment score counter
            RealMap[Pos[0], Pos[1]].collectableItem = None	#Remove coin
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
    quitting = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitting = True
        if event.type == pygame.KEYDOWN:
            if event.key == UP:
                if not RealMap[Pos[0], Pos[1]-1].solid:	#We haven't collided with anthing
                    Pos[1] -= 1
                    #scrollPos[1] -= BLOCKSIZE
            if event.key == DOWN:
                if not RealMap[Pos[0], Pos[1]+1].solid:
                    Pos[1] += 1
                    #scrollPos[1] += BLOCKSIZE
            if event.key == LEFT:
                if not RealMap[Pos[0]-1, Pos[1]].solid:
                    Pos[0] -= 1
                    #scrollPos[0] -= BLOCKSIZE
            if event.key == RIGHT:
                if not RealMap[Pos[0]+1, Pos[1]].solid:
                    Pos[0] += 1
                    #scrollPos[0] += BLOCKSIZE
            if event.key == BLAST and ExplosionValid(Pos[0], Pos[1], scores["dynamite"]):
                scores["dynamite"] = Explosion(scores["dynamite"], Pos[0], Pos[1])
            if scores["chocolate"] >= 0:
                scores["chocolate"] -= Map[Pos[0], Pos[1]].difficulty
            else:
                quitting = True
    scores = CollectItems(scores)
    return quitting, scores
    
    
def UpdateVisible():
    #CrossCheck()
    DiagonalCheck()

    
#def TestNeighbours(x, y, centreTileType):
#	if (RealMap[x, y+1] != centreTileType) and RealMap[x+1, y] != centreTileType:
#		return 
    
    
def DrawTiles():
    for x in range(Pos[0]-VISIBILITY, Pos[0]+VISIBILITY+1):
        for y in range(Pos[1]-VISIBILITY, Pos[1]+VISIBILITY+1):
            Map[x, y].draw(world, x, y)
        

def DrawPlayer(drawSurface):
    if (animCounter%9 != 0) and (Map[Pos[0], Pos[1]].top == False):
        x = (Pos[0]*BLOCKSIZE)-int(BLOCKSIZE/2)
        y = (Pos[1]*BLOCKSIZE)-int(BLOCKSIZE/2)
        radius = int(BLOCKSIZE/2)
        pygame.draw.circle(drawSurface, PLAYER1, (x, y), radius)


def DrawHud(scores, drawSurface):
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
    
    pygame.transform.scale(world, (90, (world.get_height()/world.get_width())*90), miniWorld)
    drawSurface.blit(miniWorld, (windowSize[0]-90, 302))
    miniWorldScale = 90.0/(worldSize[0]*BLOCKSIZE)
    pygame.draw.rect(drawSurface,
                     PLAYER1,
                     ((windowSize[0]-90)-(scrollPos[0]*miniWorldScale),
                      302-               (scrollPos[1]*miniWorldScale),
                      1+ (windowSize[0]-100)*miniWorldScale,
                      1+ windowSize[1]*miniWorldScale),
                     1)


def animCountUpdate(animCounter):
    if animCounter >= animLength:
        animCounter = 0
    else:
        animCounter += 1
    return animCounter
    
def setup():
    pass

def loop():
    pass

def mapWorldToScreen(scrollPos):
    window.blit(world, scrollPos)

def calculateScrollPos(scrollPos):
    playerx = (Pos[0]*BLOCKSIZE)+scrollPos[0]
    playery = (Pos[1]*BLOCKSIZE)+scrollPos[1]
    if playerx+(VISIBILITY*BLOCKSIZE) > windowSize[0]-100:         #too far right
        scrollStep = (abs((playerx+(VISIBILITY*BLOCKSIZE)) - (windowSize[0]-100)) / 2) +1
        scrollPos = (scrollPos[0]-scrollStep, scrollPos[1])
        DebugPrint("Scrolled Left" + str(scrollPos))
    if playerx-(VISIBILITY*BLOCKSIZE) < 0:                         #too far left
        scrollStep = (abs((playerx-(VISIBILITY*BLOCKSIZE))) / 2) +1
        scrollPos = (scrollPos[0]+scrollStep, scrollPos[1])
        DebugPrint("Scrolled right" + str(scrollPos))
    if playery+(VISIBILITY*BLOCKSIZE) > windowSize[1]:             #too far down
        scrollStep = (abs((playery+(VISIBILITY*BLOCKSIZE)) - windowSize[1]) / 2) +1
        scrollPos = (scrollPos[0], scrollPos[1]-scrollStep)
        DebugPrint("Scrolled up" + str(scrollPos))
    if playery-(VISIBILITY*BLOCKSIZE) < 0:                         #too far up
        scrollStep = (abs((playery-(VISIBILITY*BLOCKSIZE))) / 2) +1
        scrollPos = (scrollPos[0], scrollPos[1]+scrollStep)
        DebugPrint("Scrolled down" + str(scrollPos))

    return scrollPos
    
scrollPos = ((-BLOCKSIZE*Pos[0])+((windowSize[0]-100)/2), (-BLOCKSIZE*Pos[1])+(windowSize[1]/2))
DebugPrint("Initial scrollPos" + str(scrollPos))
  
quitting = False
while not quitting:
    time.sleep(0.04)
    quitting, scores = HandleEvents(scores)
    UpdateVisible()
    DrawTiles()
    DrawPlayer(world)
    scrollPos = calculateScrollPos(scrollPos)
    mapWorldToScreen(scrollPos)
    DrawHud(scores, window)
    animCounter = animCountUpdate(animCounter)
    pygame.display.update()
            
pygame.quit()
sys.exit()