import pygame
import collectables
from directions import *

'''Load and convert all in-game images'''

# Size of terrain sprites.
TILESIZE = 12

# Images with transparency use convert_alpha().

# Terrain sprites.
Water = pygame.image.load("tiles/Water.png").convert()
DeepWater = pygame.image.load("tiles/DeepWater.png").convert()
Rock = pygame.image.load("tiles/Rock.png").convert()
Paving = pygame.image.load("tiles/Paving.png").convert()
Floor = pygame.image.load("tiles/Floor.png").convert()
Grass = pygame.image.load("tiles/Grass.png").convert()
Marsh = pygame.image.load("tiles/Marsh.png").convert()
Wall = pygame.image.load("tiles/Wall.png").convert()
Glass = pygame.image.load("tiles/Glass.png").convert()
Wood = pygame.image.load("tiles/Wood.png").convert()
Trees = pygame.image.load("tiles/Trees.png").convert()
Sand = pygame.image.load("tiles/Sand.png").convert()
Snow = pygame.image.load("tiles/Snow.png").convert()

# Overlays for unknown, non-visible, damaged or burning tiles.
Unknown = pygame.image.load("tiles/Unknown.png").convert()
NonVisible = pygame.image.load("tiles/NonVisible.png").convert_alpha()
Damaged = pygame.image.load("tiles/Damaged.png").convert_alpha()
Burning = pygame.image.load("tiles/Fire.png").convert()

# Overlays for tiles with collectables.
Coin = pygame.image.load("tiles/Coin.png").convert_alpha()
Choc = pygame.image.load("tiles/Chocolate.png").convert_alpha()
Dynamite = pygame.image.load("tiles/Dynamite.png").convert_alpha()

Collectables = {
    collectables.COIN: Coin,
    collectables.CHOCOLATE: Choc,
    collectables.DYNAMITE: Dynamite
}

# Player sprites.
PlayerUp = pygame.image.load("tiles/Player.png").convert_alpha()
PlayerDown = pygame.transform.flip(PlayerUp, False, True)
PlayerLeft = pygame.transform.rotate(PlayerUp, 90)
PlayerRight = pygame.transform.flip(PlayerLeft, True, False)

Player = {
    UP: PlayerUp,
    DOWN: PlayerDown,
    LEFT: PlayerLeft,
    RIGHT: PlayerRight
}

# Bear sprites.
BearLeft = pygame.image.load("tiles/Bear.png").convert_alpha()
BearRight = pygame.transform.flip(BearLeft, True, False)

# Dragon sprites.
DragonRedUpLeft = pygame.image.load("tiles/Dragon-Red.png").convert_alpha()
DragonRedUpRight = pygame.transform.flip(DragonRedUpLeft, True, False)
DragonRedDownLeft = pygame.transform.flip(DragonRedUpLeft, False, True)
DragonRedDownRight = pygame.transform.flip(DragonRedUpLeft, True, True)

DragonRed = {
    UPLEFT: DragonRedUpLeft,
    UPRIGHT: DragonRedUpRight,
    DOWNLEFT: DragonRedDownLeft,
    DOWNRIGHT: DragonRedDownRight
}
