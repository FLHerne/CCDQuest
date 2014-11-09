import imghdr
import os
import pygame
import collectables
import terrain
from colors import MAGENTA
from directions import *

"""Load and convert all in-game images"""

# Size of terrain sprites.
TILESIZE = 12

# Images with transparency use convert_alpha().

terraingroups = {}
for name in os.listdir(os.path.join('tiles', 'terrain')):
    if not os.path.isdir(os.path.join('tiles', 'terrain', name)):
        continue
    if not (name in terrain.types['groundimage'] or name in terrain.types['topimage']):
        print "Warning: terrain sprites", name, "not used"
    terraingroups[name] = []
    for filename in os.listdir(os.path.join('tiles', 'terrain', name)):
        filepath = os.path.join('tiles', 'terrain', name, filename)
        if imghdr.what(filepath) == 'png':
            loadedimage = pygame.image.load(filepath).convert()
            loadedimage.set_colorkey(MAGENTA, pygame.RLEACCEL)
            terraingroups[name].append(loadedimage)

numtypes = len(terrain.types)
indexedterrain = [(0, None)]
for i in enumerate(terrain.types['groundimage']):
    offsetgroup = (numtypes/2 - i[0], terraingroups[i[1]]) if i[1] else (0, None)
    indexedterrain.append(offsetgroup)
for i in enumerate(terrain.types['topimage']):
    offsetgroup = (numtypes/2 - i[0], terraingroups[i[1]]) if i[1] else (0, None)
    indexedterrain.append(offsetgroup)

# Overlays for unknown, non-visible, damaged or burning tiles.
Unknown = pygame.image.load("tiles/overlays/Unknown.png").convert()
NonVisible = pygame.image.load("tiles/overlays/NonVisible.png").convert_alpha()

# These two can be randomly chosen
Damaged = [
    pygame.image.load("tiles/overlays/damaged/Damaged1.png").convert_alpha(),
    pygame.image.load("tiles/overlays/damaged/Damaged2.png").convert_alpha(),
    pygame.image.load("tiles/overlays/damaged/Damaged3.png").convert_alpha(),
    pygame.image.load("tiles/overlays/damaged/Damaged4.png").convert_alpha()
]

Burning = [
    pygame.image.load("tiles/overlays/fire/Fire1.png").convert_alpha(),
    pygame.image.load("tiles/overlays/fire/Fire2.png").convert_alpha(),
    pygame.image.load("tiles/overlays/fire/Fire3.png").convert_alpha(),
    pygame.image.load("tiles/overlays/fire/Fire4.png").convert_alpha()
]

# Overlays for fuses.
FuseLeft = pygame.image.load("tiles/overlays/Fuse.png").convert_alpha()
FuseRight = pygame.transform.rotate(FuseLeft, 180)
FuseUp = pygame.transform.rotate(FuseLeft, -90)
FuseDown = pygame.transform.rotate(FuseLeft, 90)

Fuse = {
    UP: FuseUp,
    DOWN: FuseDown,
    LEFT: FuseLeft,
    RIGHT: FuseRight
}


# Overlays for tiles with collectables.
Coin = pygame.image.load("tiles/collectables/Coin.png").convert_alpha()
Choc = pygame.image.load("tiles/collectables/Chocolate.png").convert_alpha()
Dynamite = pygame.image.load("tiles/collectables/Dynamite.png").convert_alpha()

Collectables = {
    collectables.COIN: Coin,
    collectables.CHOCOLATE: Choc,
    collectables.DYNAMITE: Dynamite
}

# Player sprites.
PlayerUp = pygame.image.load("tiles/gemgos/Player.png").convert_alpha()
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
BearLeft = pygame.image.load("tiles/gemgos/Bear.png").convert_alpha()
BearRight = pygame.transform.flip(BearLeft, True, False)

# Dragon sprites.
DragonRedUpLeft = pygame.image.load("tiles/gemgos/Dragon-Red.png").convert_alpha()
DragonRedUpRight = pygame.transform.flip(DragonRedUpLeft, True, False)
DragonRedDownLeft = pygame.transform.flip(DragonRedUpLeft, False, True)
DragonRedDownRight = pygame.transform.flip(DragonRedUpLeft, True, True)

DragonRed = {
    UPLEFT: DragonRedUpLeft,
    UPRIGHT: DragonRedUpRight,
    DOWNLEFT: DragonRedDownLeft,
    DOWNRIGHT: DragonRedDownRight
}

Sign = pygame.image.load("tiles/gemgos/Sign.png").convert_alpha()
PixieLeft = pygame.image.load("tiles/gemgos/Pixie.png").convert_alpha()
PixieRight = pygame.transform.flip(PixieLeft, True, False)

