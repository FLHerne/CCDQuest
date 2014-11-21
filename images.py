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

def dirsprites(image):
    sprites = []
    for i in range(6):
        sprites.append(pygame.Surface((loadedimage.get_height(),)*2))
        sprites[-1].blit(loadedimage, (-i*loadedimage.get_height(), 0))
        sprites[-1].set_colorkey(MAGENTA, pygame.RLEACCEL)
    rot = pygame.transform.rotate
    #FIXME Horribly ugly!
    return [
            sprites[0],       #0
            sprites[1],
        rot(sprites[1], 90),
            sprites[2],
        rot(sprites[1], 180), #4
            sprites[3],
        rot(sprites[2], 90),
            sprites[4],
        rot(sprites[1], 270), #8
        rot(sprites[2], 270),
        rot(sprites[3], 90),
        rot(sprites[4], 270),
        rot(sprites[2], 180), #12
        rot(sprites[4], 180),
        rot(sprites[4], 90),
            sprites[5]
        ]

terraingroups = {}
# Create list of sprites and/or of 16-sprite direction lists for each subdirectory of tiles/terrain.
for name in os.listdir(os.path.join('tiles', 'terrain')):
    if not os.path.isdir(os.path.join('tiles', 'terrain', name)):
        continue
    if not (name in terrain.types['groundimage'] or name in terrain.types['topimage']):
        print "Warning: terrain sprites", name, "not used"
    terraingroups[name] = []
    for filename in os.listdir(os.path.join('tiles', 'terrain', name)):
        filepath = os.path.join('tiles', 'terrain', name, filename)
        if not imghdr.what(filepath) == 'png':
            continue
        loadedimage = pygame.image.load(filepath).convert()
        numtiles = float(loadedimage.get_width())/loadedimage.get_height()
        if numtiles not in [1, 6]:
            print "Warning: sprite", filepath, "has invalid size"
            continue
        if numtiles == 1:
            loadedimage.set_colorkey(MAGENTA, pygame.RLEACCEL)
            terraingroups[name].append(loadedimage)
        else:
            terraingroups[name].append(dirsprites(loadedimage))
            continue

# Create list of all sprites used, in format (layeroffset, surface).
# Create list of sprite indices and/or of 16-index direction lists of indices...
# ...for each tile type in each of terrain.indexmaps['groundimage'] and ...['topimage'].
numtypes = len(terrain.types)
indexedterrain = [(0, None)]
for level in ['groundimage', 'topimage']:
    for i in enumerate(terrain.types[level]):
        levelmap = terrain.typetoimageindex[level]
        levelmap.append([])
        if not i[1]:
            levelmap[i[0]].append(0)
            continue
        group = terraingroups[i[1]]
        offset = numtypes/2 - i[0]
        directionlists = []
        directionlists = filter(lambda a: isinstance(a, list), group)
        othersprites = filter(lambda a: not isinstance(a, list), group)
        for sprite in othersprites:
            index = len(indexedterrain)
            indexedterrain.append((offset, sprite))
            levelmap[i[0]].append(index)
        for dirlist in directionlists:
            index = len(indexedterrain)
            indexedterrain += [(offset, sprite) for sprite in dirlist]
            levelmap[i[0]].append(range(index, index+16))


# Images with transparency use convert_alpha().

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
Portal = pygame.image.load("tiles/gemgos/Portal.png").convert_alpha()
PixieLeft = pygame.image.load("tiles/gemgos/Pixie.png").convert_alpha()
PixieRight = pygame.transform.flip(PixieLeft, True, False)

DuckieLeft = pygame.image.load("tiles/gemgos/Duckie.png").convert_alpha()
DuckieRight = pygame.transform.flip(DuckieLeft, True, False)