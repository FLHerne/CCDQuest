import pygame
import collectables
from directions import *

'''Load and convert all in-game images'''

# Size of terrain sprites.
TILESIZE = 12

# Images with transparency use convert_alpha().

# Terrain sprites.
Terrain = [
    [pygame.image.load("tiles/Water.png").convert(),],
    [pygame.image.load("tiles/DeepWater.png").convert(),],
    [
        pygame.image.load("tiles/Rock1.png").convert(),
        pygame.image.load("tiles/Rock2.png").convert(),
        pygame.image.load("tiles/Rock3.png").convert(),
        pygame.image.load("tiles/Rock4.png").convert(),
    ],
    [pygame.image.load("tiles/Paving.png").convert(),],
    [pygame.image.load("tiles/Floor.png").convert(),],
    [
        pygame.image.load("tiles/Grass1.png").convert(),
        pygame.image.load("tiles/Grass2.png").convert(),
        pygame.image.load("tiles/Grass3.png").convert(),
        pygame.image.load("tiles/Grass4.png").convert(),
        pygame.image.load("tiles/Grass5.png").convert()
    ],
    [pygame.image.load("tiles/Marsh.png").convert(),],
    [pygame.image.load("tiles/Wall.png").convert(),],
    [pygame.image.load("tiles/Glass.png").convert(),],
    [pygame.image.load("tiles/Wood.png").convert(),],
    [
        pygame.image.load("tiles/Trees1.png").convert(),
        pygame.image.load("tiles/Trees2.png").convert(),
        pygame.image.load("tiles/Trees3.png").convert(),
        pygame.image.load("tiles/Trees4.png").convert(),
        pygame.image.load("tiles/Trees5.png").convert(),
        pygame.image.load("tiles/Trees6.png").convert(),
        pygame.image.load("tiles/Trees7.png").convert(),
        pygame.image.load("tiles/Trees8.png").convert(),
    ],
    [pygame.image.load("tiles/Sand.png").convert(),],
    [
        pygame.image.load("tiles/Snow1.png").convert(),
        pygame.image.load("tiles/Snow2.png").convert(),
        pygame.image.load("tiles/Snow3.png").convert(),
        pygame.image.load("tiles/Snow4.png").convert(),
    ]
]

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

Sign = pygame.image.load("tiles/Sign.png").convert_alpha()