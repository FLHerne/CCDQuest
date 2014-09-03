#!/usr/bin/env python2.6

'''Game of exploration in a grid-based world'''

import pygame
import sys
import time
import copy
import TextBox
import newTextBox
import random

from colours import *

# -----------------------------------------------------------------------------

printDebug = True
printError = True

def DebugPrint(Message):            # Messages which the end-user need not see, but may be useful to the developer
    if printDebug:
        print(Message)
 
def ErrorPrint(Message):            # Messages which indicate that something has gone wrong
    if printError:
        print("Error: " + Message)

# -----------------------------------------------------------------------------
  
#groundFile = 'map/smallMap-ground.png'                # Image to use as map
#collectablesFile = 'map/smallMap-collectables.png'
groundFile = 'map/World7-ground.png'                   # Image to use as map
collectablesFile = 'map/World7-collectables.png'
#groundFile = 'map/latestRandomGen.png'                # Image to use as map
#collectablesFile = 'map/blank.png'

ground = pygame.image.load(groundFile)
collectables = pygame.image.load(collectablesFile)
worldSize = ground.get_rect().size
worldSize = [worldSize[0], worldSize[1]]
BLOCKSIZE = 8                       # Size of each square in the grid
VISIBILITY = 15                     # How far can you see in an approximate circle
HUDFONTSIZE = 20                    # Score counter etc
totalCoins = 0                      # How many coins are there in total? (initialise)
windowSize = (740, 480)

scores = {"coins" : 0,
          "chocolate" : 10000, 
          "dynamite" : 15}

animCounter = 0
animLength = 36

window = pygame.display.set_mode(windowSize)
world = pygame.Surface((worldSize[0]*BLOCKSIZE, worldSize[1]*BLOCKSIZE))

import images

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
NonVisibleImage = pygame.image.load("tiles/NonVisible.png")     # An overlay for no-longer-visible tiles

DamageImage = pygame.image.load("tiles/Damage.png")             # An overlay for damaged (blown-up) tiles
DamageImage = DamageImage.convert_alpha()                       # this image is transparent, so the alpha must be used too





BearImageLeft = pygame.image.load("tiles/bear.png")
BearImageRight = pygame.transform.flip(BearImageLeft, True, False)

collectablesImages = { 1 : images.Coin,                           # semi-enum for referencing collectable images
                       2 : images.Choc,
                       3 : images.Dynamite}
  
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
        DrawPos = (x*BLOCKSIZE, y*BLOCKSIZE)
        if not self.explored:
            drawSurface.blit(UnknownImage, DrawPos)
            return
        drawSurface.blit(self.image, DrawPos)
        if self.damaged:
            drawSurface.blit(DamageImage, DrawPos)
        if self.collectableItem != None:
            drawSurface.blit(collectablesImages[self.collectableItem], DrawPos)
        if not self.visible:
            drawSurface.blit(NonVisibleImage, DrawPos)

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
        

# -----------------------------------------------------------------------------

class ModDict(dict):
    '''A hacked dict that wraps tuples that look like coordinates to the world size - approach with caution!'''
    def __init__(self, *args):
        dict.__init__(self, args)
    def __getitem__(self, key):
        return dict.__getitem__(self, (key[0] % worldSize[0], key[1] % worldSize[1]))
    def __setitem__(self, key, val):
        dict.__setitem__(self, (key[0] % worldSize[0], key[1] % worldSize[1]), val)
    def __delitem__(self, key):
        dict.__delitem__(self, (key[0] % worldSize[0], key[1] % worldSize[1]))

RealMap = ModDict()

groundMap = pygame.PixelArray(ground)
collectablesMap = pygame.PixelArray(collectables)

def PopulateMap(groundMap, collectablesMap):
    '''create an array of cells from bitmaps'''
    worldSize = ground.get_rect().size
    worldSize = [worldSize[0], worldSize[1]]

    for x in range(0, worldSize[0]):
        for y in range(0, worldSize[1]):
            groundColour = ground.unmap_rgb(groundMap[x, y])
            RealMap[x, y] = copy.copy(UnMapGroundColour(groundColour))
            collectableColour = collectables.unmap_rgb(collectablesMap[x, y])
            RealMap[x, y].collectableItem = UnMapCollectablesColour(collectableColour)
            if collectableColour == START:
                DebugPrint("Found starting position")
                Pos = [x, y]
    if Pos is None:
        ErrorPrint("No starting position defined")

    del groundMap
    del collectablesMap
    
    return RealMap, Pos
    
def CountCoins(RealMap, rect=pygame.Rect((0, 0), (worldSize[0], worldSize[1]))):
    '''Count the number of cells containing coins in the given region of map'''
    totalCoins = 0
    for x in range(rect.left, rect.right+1):
        for y in range(rect.top, rect.bottom+1):
            if RealMap[x, y].collectableItem == Cell.COIN:
                totalCoins += 1
    return totalCoins
   
RealMap, Pos = PopulateMap(groundMap, collectablesMap)
totalCoins = CountCoins(RealMap) 

# -----------------------------------------------------------------------------
        
window.fill(GREY)
world.fill(GREY)
miniWorld = pygame.transform.scale(world, (90, (world.get_height()/world.get_width())*90))

# -----------------------------------------------------------------------------

def DiagonalCheck():
    '''Test visibility along (offset) diagronals away from player'''
    x = Pos[0]
    y = Pos[1]
    RealMap[x, y].explored = True                       # make the currently occupied cell visible
    RealMap[x, y].visible = True
    for horizontal in (True, False):                # horizontal and vertical
        for Dir1 in (-1, 1):                        # left/right or up/down
            for Dir2 in (-1, 1):                    # final division into octants
                Base = 0                            # how far horizontally or vertically the test ray is from the player
                while (abs(Base) < VISIBILITY and
                    RealMap[Pos[0]+(Base if horizontal else 0),
                        Pos[1]+(0 if horizontal else Base)].transparent):   # repeatedly test if a cell is transparent and within a bounding square
                    #Base += Dir1       #FIXME - either the main diagonals aren't shown, or the ends of the cross aren't
                    if horizontal:
                        x = Pos[0] + Base
                        y = Pos[1]
                    else:
                        x = Pos[0]
                        y = Pos[1] + Base
                    RealMap[x, y].explored = True
                    RealMap[x, y].visible = True
                    while RealMap[x, y].transparent and ((Pos[1]-y)**2) + ((Pos[0]-x)**2) <= VISIBILITY**2: # test in bounding circle
                        if horizontal:                                                                      # move diagonally
                            x += Dir1
                            y += Dir2
                        else:
                            x += Dir2
                            y += Dir1
                        RealMap[x, y].explored = True                                                           # make visible
                        RealMap[x, y].visible = True
                    RealMap[x, y].explored = True                                                               # make the first opaque cell visible too
                    RealMap[x, y].visible = True
                    Base += Dir1       #FIXME - either the main diagonals aren't shown, or the ends of the cross aren't
                RealMap[x, y].explored = True
                RealMap[x, y].visible = True
                
# -----------------------------------------------------------------------------

def CrossCheck():
    '''Check visibility straight up, down, left and right'''
    for i in (-1, 1):                                                           # Horizontally left and right
        X = 0                                                                   # start at the player      
        while RealMap[(X*i)+Pos[0], Pos[1]].transparent and X < VISIBILITY:     # if transparent and within bounding range

            RealMap[(X*i)+Pos[0], Pos[1]].explored = True           # make visible
            RealMap[(X*i)+Pos[0], Pos[1]].visible = True
            X += 1                                                              # move away from player
        RealMap[(X*i)+Pos[0], Pos[1]].explored = True               # make final cell visible
        RealMap[(X*i)+Pos[0], Pos[1]].visible = True

    for i in (-1, 1):                                                           # Repeat as above, but vertically
        Y = 0
        while RealMap[Pos[0], (Y*i)+Pos[1]].transparent and Y < VISIBILITY:
            RealMap[Pos[0], (Y*i)+Pos[1]].explored = True
            RealMap[Pos[0], (Y*i)+Pos[1]].visible = True
            Y += 1
        RealMap[Pos[0], (Y*i)+Pos[1]].explored = True
        RealMap[Pos[0], (Y*i)+Pos[1]].visible = True

class Bear:
    def __init__(self, position):
        self.position = list(position)
        self.direction = -1 # Left
    def hunt(self):
        if abs(Pos[0]-self.position[0]) + abs(Pos[1]-self.position[1]) > 15:
            return False
        def worldPos(d_coord):
            return (self.position[0] + d_coord[0] - 32,
                    self.position[1] + d_coord[1] - 32)
        def isTarget(d_coord):
            return (worldPos(d_coord)[0]%worldSize[0] == Pos[0]%worldSize[0] and
                    worldPos(d_coord)[1]%worldSize[1] == Pos[1]%worldSize[1])

        foundtarget = False
        dijkstramap = [[(512, (32, 32)) for x in xrange(64)] for x in xrange(64)]
        import heapq
        openlist = []
        heapq.heappush(openlist, (0, (32, 32)))
        curp = False
        while openlist:
            curn = heapq.heappop(openlist)
            curd = curn[0]
            curp = curn[1]
            print "CurP is", curp
            if isTarget(curp):
                foundtarget = True
                break
            for nbrpos in [(curp[0]-1,curp[1]), (curp[0],curp[1]-1), (curp[0]+1,curp[1]), (curp[0],curp[1]+1)]:
                if nbrpos[0] < 0 or nbrpos[1] < 0 or nbrpos[0] >= 64 or nbrpos[1] >= 64:
                    continue
                if dijkstramap[nbrpos[0]][nbrpos[1]][0] != 512 or RealMap[worldPos(nbrpos)].solid:
                    continue
                dijkstramap[nbrpos[0]][nbrpos[1]] = (curd+1, curp)
                heapq.heappush(openlist, (curd+1, nbrpos))
        if not foundtarget:
            print "Failed"
            return False
        print "Success"
        while dijkstramap[curp[0]][curp[1]][1] != (32, 32):
            curp = dijkstramap[curp[0]][curp[1]][1]
        self.position[0] += curp[0]-32
        self.direction = curp[0]-32 if abs(curp[0]-32) else self.direction
        self.position[1] += curp[1]-32
        return True
    
    def draw(self, drawSurface):
        if RealMap[self.position].top or not RealMap[self.position].visible:
            return
        x = ((self.position[0]*BLOCKSIZE))
        y = ((self.position[1]*BLOCKSIZE))
        drawSurface.blit(BearImageRight if self.direction > 0 else BearImageLeft, (x, y))

def placeBears(number):
    max_attempts = 20*number
    created = []
    for i in xrange(max_attempts):
        attempt = (random.randint(0,worldSize[0]-1), random.randint(0,worldSize[1]-1))
        if RealMap[attempt].name not in ['turf', 'forrest', 'rocky ground']:
            continue
        created.append(Bear(attempt))
        if len(created) == number:
            break
    return created

def moveBears(bearlist):
    for bear in bearlist:
        bear.hunt()

def drawBears(bearlist, drawSurface):
    for bear in bearlist:
        bear.draw(drawSurface)

bears = placeBears(int(worldSize[0]*worldSize[1]/5000))

def ExplosionValid(x, y, Dynamite):
    '''test if an explosion is currently possible'''
    global currentMessage
    if (Dynamite <=0):
        DebugPrint("No Dynamite:")
        currentMessage = "You look, but find you have no dynamite left"
    if not RealMap[x, y].destructable:
        DebugPrint("Current cell cannot be destroyed")
        currentMessage = "Explosives won't work here"
    if (Dynamite > 0 and RealMap[x, y].destructable):
        DebugPrint("Explosion possible")
    else:
        DebugPrint("Explosion not possible")
    return (Dynamite > 0 and RealMap[x, y].destructable)
        
        
def Explosion(Dynamite, Centrex, Centrey):
    '''Clear a 3x3 square using a stick of dynamite'''
    global currentMessage
    DebugPrint("Explosion at " + str(Centrex) + ", " + str(Centrey))
    currentMessage = "BANG!"
    for x in (-1, 0, 1):                                                        # explosion forms a 3x3 square
        for y in (-1, 0, 1):
            RealMap[Centrex, Centrey].collectableItem = None
            if RealMap[Centrex+x, Centrey+y].collectableItem == Cell.DYNAMITE:
                Explosion(1, Centrex+x, Centrey+y)                              # dynamite sets off neighbouring dynamite
                currentMessage = "The dynamite sets off a chain reaction"
            if RealMap[Centrex+x, Centrey+y].destructable:
                RealMap[Centrex+x, Centrey+y].solid = False
                RealMap[Centrex+x, Centrey+y].transparent = True
                RealMap[Centrex+x, Centrey+y].damaged = True
                RealMap[Centrex+x, Centrey+y].difficulty += 5
                if not ((x, y) == (0, 0)):
                    RealMap[Centrex+x, Centrey+y].name = "debris from an explosion"
                if RealMap[Centrex+x, Centrey+y].image == images.Wood:
                    RealMap[Centrex+x, Centrey+y].image = images.Water
    Dynamite -= 1
    return Dynamite
    
def TestArea(centrex, centrey, name):
    '''test the space around a point for particular cell names'''
    count = 0
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if RealMap[centrex+x, centrey+y].name == name:
                count += 1
    return count
    
    
def updateContextMessages(x, y, currentMessage):
    '''Generate context-based commentary'''
    if TestArea(x, y, "window") > 1:
        currentMessage = "You peer through the window"
    elif TestArea(x, y, "snow") > 3:
        currentMessage = "The snow looks cold"
    elif TestArea(x, y, "water") > 3:
        currentMessage = "The water looks wet"
    elif TestArea(x, y, "forrest") > 2:
        currentMessage = "The trees look foreboding"
    elif TestArea(x, y, "forrest") > 6:
        currentMessage = "You are surrounded by trees"
    if RealMap[x, y].top:
        currentMessage = "You stumble blindly through the darkness"
    if RealMap[x, y].temperature < 15:
        if RealMap[x, y].temperature < 0:
            currentMessage = "The icy air makes you thankful that you packed a wooley jumper"
        else:
            currentMessage = "Its a bit chilly here"
    if RealMap[x, y].damaged and moved:
        currentMessage = "The debris is unstable underfoot"
    if newTerrain:
        if (random.randint(0, 50) < RealMap[x, y].difficulty):
            currentMessage = "Is this " + str(RealMap[x, y].name) + " safe?"
        else:
            currentMessage = "You reach some " + str(RealMap[x, y].name)
    if (random.randint(0, 1000) < RealMap[x, y].difficulty):
        currentMessage = "Is this " + str(RealMap[x, y].name) + " really safe?"
    return currentMessage
    
    
def CollectItems(scores):
    '''deal with any colllectables found on the current cell'''
    global currentMessage
    if RealMap[Pos[0], Pos[1]].collectableItem == Cell.COIN:    #Have we just walked into a coin
        scores["coins"] += 1                                    #Increment score counter
        RealMap[Pos[0], Pos[1]].collectableItem = None          #Remove coin
        DebugPrint("Collected a coin")
        currentMessage = "You find a gold coin"
    if RealMap[Pos[0], Pos[1]].collectableItem == Cell.DYNAMITE:
        scores["dynamite"] += 1
        RealMap[Pos[0], Pos[1]].collectableItem = None
        DebugPrint("Collected a stick of dynamite")
        currentMessage = "You collect some dynamite"
    if RealMap[Pos[0], Pos[1]].collectableItem == Cell.CHOCOLATE:
        scores["chocolate"] += 50
        RealMap[Pos[0], Pos[1]].collectableItem = None
        DebugPrint("Collected a bar of chocolate")
        currentMessage = "You pick up the bar of chocolate"
    return scores

        
def HandleEvents(scores, moved):
    '''respond to user input'''
    global oldTerrainName
    global newTerrain
    newTerrain = False
    quitting = False
    moved = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitting = True
        if event.type == pygame.KEYDOWN:
            if random.random() < 0.7:
                moveBears(bears)
            if event.key == UP:
                if not RealMap[Pos[0], Pos[1]-1].solid: #We haven't collided with anthing
                    Pos[1] -= 1
                    moved = True
            if event.key == DOWN:
                if not RealMap[Pos[0], Pos[1]+1].solid:
                    Pos[1] += 1
                    moved = True
            if event.key == LEFT:
                if not RealMap[Pos[0]-1, Pos[1]].solid:
                    Pos[0] -= 1
                    moved = True
            if event.key == RIGHT:
                if not RealMap[Pos[0]+1, Pos[1]].solid:
                    Pos[0] += 1
                    moved = True
            if event.key == BLAST and ExplosionValid(Pos[0], Pos[1], scores["dynamite"]):
                scores["dynamite"] = Explosion(scores["dynamite"], Pos[0], Pos[1])
            if scores["chocolate"] >= 0:
                scores["chocolate"] -= RealMap[Pos[0], Pos[1]].difficulty
            else:
                quitting = True
    newTerrainName = RealMap[Pos[0], Pos[1]].name
    if newTerrainName != oldTerrainName:
        newTerrain = True
        DebugPrint("Terrain type change (" + newTerrainName + " --> " + oldTerrainName + ")")
    oldTerrainName = newTerrainName
    scores = CollectItems(scores)
    return quitting, scores, moved
    
    
def UpdateVisible():
    '''update the visibility of cells by the player'''
    for x in range(Pos[0]-VISIBILITY-1, Pos[0]+VISIBILITY+2):
        for y in range(Pos[1]-VISIBILITY-1, Pos[1]+VISIBILITY+2):
            RealMap[x, y].visible = False
    CrossCheck()
    DiagonalCheck()
    
    
def DrawTiles():
    '''redraw every cell that might be visible or have been visible on the previous draw'''
    for x in range(Pos[0]-VISIBILITY-1, Pos[0]+VISIBILITY+2):
        for y in range(Pos[1]-VISIBILITY-1, Pos[1]+VISIBILITY+2):
            RealMap[x, y].draw(world, x%worldSize[0], y%worldSize[1])
        

def DrawPlayer(drawSurface):
    '''draw the player as a blinking circle'''
    if (animCounter%9 != 0) and (RealMap[Pos[0], Pos[1]].top == False):
        x = ((Pos[0]*BLOCKSIZE)+int(BLOCKSIZE/2))
        y = ((Pos[1]*BLOCKSIZE)+int(BLOCKSIZE/2))
        radius = int(BLOCKSIZE/2)
        pygame.draw.circle(drawSurface, PLAYER1, (x%world.get_width(), y%world.get_height()), radius)

def DrawMessageBox(drawSurface):
    '''Draw the box containing the most recent user-facing message'''
    messageBoxHeight = 20
    sidePanelWidth = 95
    messageBoxRect = pygame.Rect((0,  windowSize[1]-messageBoxHeight), (windowSize[0]-sidePanelWidth, messageBoxHeight))
    pygame.draw.rect(drawSurface, BLACK, messageBoxRect)
    newTextBox.Draw(drawSurface, currentMessage, messageBoxRect)
        
def DrawHud(scores, drawSurface):
    '''Draw the heads-up display, with current information'''
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
    old_clip = window.get_clip()
    window.set_clip((windowSize[0]-90, 302, 90, 90))
    pygame.transform.scale(world, (90, (world.get_height()/world.get_width())*90), miniWorld)
    drawSurface.blit(miniWorld, (windowSize[0]-90, 302))
    miniWorldScale = 90.0/(worldSize[0]*BLOCKSIZE)
    for tx in [scrollPos[0]-world.get_width(), scrollPos[0], scrollPos[0]+world.get_width()]:
        for ty in [scrollPos[1]-world.get_height(), scrollPos[1], scrollPos[1]+world.get_height()]:
            pygame.draw.rect(drawSurface,
                PLAYER1,
                ((windowSize[0]-90)-(tx*miniWorldScale), # Top x corner of minimap, plus scroll offset
                302-                (ty*miniWorldScale), # Top y ''
                1+ (windowSize[0]-100)*miniWorldScale,
                1+ windowSize[1]*miniWorldScale),
                1)
    window.set_clip(old_clip)
    
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
    if scores["coins"] >= totalCoins:
        TextBox.Print(drawSurface,
                      False,
                      0, 0,
                      windowSize[0],
                      BLACK,
                      WHITE,
                      'Arial', HUDFONTSIZE*2,
                      "You found all the coins!",
                      True,
                      [True, windowSize[1]])


def animCountUpdate(animCounter):
    '''a looping counter for crude animation'''
    if animCounter >= animLength:
        animCounter = 0
    else:
        animCounter += 1
    return animCounter

def wrapCoords(scrollPos):
    '''allow player to walk around the world in a loop'''
    playerx = (Pos[0]*BLOCKSIZE)+scrollPos[0]
    playery = (Pos[1]*BLOCKSIZE)+scrollPos[1]
    if Pos[0] % worldSize[0] == int(worldSize[0]/2):
        Pos[0] %= worldSize[0]
    if Pos[1] % worldSize[1] == int(worldSize[1]/2):
        Pos[1] %= worldSize[1]
    return ((-BLOCKSIZE*Pos[0])+playerx, (-BLOCKSIZE*Pos[1])+playery)
    
def setup():
    '''to be used at the beginning of the programme'''
    pass

def loop():
    '''to be used repeatedly'''
    pass

def mapWorldToScreen(scrollPos):
    '''show part of the world on screen'''
    old_clip = window.get_clip()
    worldRegion = pygame.Rect(0, 0, windowSize[0]-90, windowSize[1]-20)
    window.set_clip(worldRegion)
    for tx in [scrollPos[0]-world.get_width(), scrollPos[0], scrollPos[0]+world.get_width()]:
        for ty in [scrollPos[1]-world.get_height(), scrollPos[1], scrollPos[1]+world.get_height()]:
            if world.get_rect(topleft=(tx, ty)).colliderect(worldRegion):
                window.blit(world, (tx, ty))
    window.set_clip(old_clip)

def calculateScrollPos(scrollPos):
    '''scroll towards the correct position'''
    playerx = (Pos[0]*BLOCKSIZE)+scrollPos[0]
    playery = (Pos[1]*BLOCKSIZE)+scrollPos[1]
    if playerx+(VISIBILITY*BLOCKSIZE) > windowSize[0]-100:         #too far right
        scrollStep = (abs((playerx+(VISIBILITY*BLOCKSIZE)) - (windowSize[0]-100)) / 2) +1
        scrollPos = (scrollPos[0]-scrollStep, scrollPos[1])
        DebugPrint(str(Pos))
        DebugPrint("Scrolled Left" + str(scrollPos))
    if playerx-(VISIBILITY*BLOCKSIZE) < 0:                         #too far left
        scrollStep = (abs((playerx-(VISIBILITY*BLOCKSIZE))) / 2) +1
        scrollPos = (scrollPos[0]+scrollStep, scrollPos[1])
        DebugPrint(str(Pos))
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
currentMessage = "You find yourself in the middle of a strange and unknown landscape"
moved = False
newTerrain = False
oldTerrainName = "paving"

quitting = False
while not quitting:
    time.sleep(0.04)
    quitting, scores, moved = HandleEvents(scores, moved)
    UpdateVisible()
    DrawTiles()
    DrawPlayer(world)
    drawBears(bears, world)
    scrollPos = calculateScrollPos(scrollPos)
    mapWorldToScreen(scrollPos)
    scrollPos = wrapCoords(scrollPos)
    currentMessage = updateContextMessages(Pos[0], Pos[1], currentMessage)
    DrawMessageBox(window)
    DrawHud(scores, window)
    animCounter = animCountUpdate(animCounter)
    
    #newTextBox.Draw(window, "Hello, World!", pygame.Rect((30, 30), (200, 50)))
    
    pygame.display.update()
            
pygame.quit()
sys.exit()