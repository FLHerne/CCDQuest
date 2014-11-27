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

def chopimage(image, xslices, yslices=1):
    """Chop an image into a line or grid of smaller images"""
    outrect = pygame.Rect(0, 0, image.get_width()/xslices, image.get_height()/yslices)
    chopped = []
    for ix in range(xslices):
        chopped.append([])
        for iy in range(yslices):
            choprect = outrect.move(ix*outrect.width, iy*outrect.height)
            chopped[-1].append(image.subsurface(choprect))
    # Return a 1d array if only chopping in X axis.
    return [sub[0] for sub in chopped] if yslices == 1 else chopped

def dirsprites(image):
    sprites = chopimage(image, 6)
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

def pathimage(*path, **kwargs):
    convfunc = pygame.Surface.convert_alpha if ('alpha' in kwargs and kwargs['alpha']) else pygame.Surface.convert
    return convfunc(pygame.image.load(os.path.join(*path)))

def getimages(dirpath, alpha=False, colorkey=None):
    assert not (alpha and colorkey)
    images = []
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        if not imghdr.what(filepath) == 'png':
            continue
        image = pathimage(filepath, alpha=alpha)
        image.set_colorkey(colorkey)
        images.append(image)
    return images

def subdirs(dirpath):
    """Paths to subdirectories of 'dirpath'"""
    return filter(os.path.isdir, [os.path.join(dirpath, name) for name in os.listdir(dirpath)])

terraingroups = {}
# Create list of sprites and/or of 16-sprite direction lists for each subdirectory of tiles/terrain.
for terraindir in subdirs(os.path.join('tiles', 'terrain')):
    name = os.path.basename(terraindir)
    if not (name in terrain.types['groundimage'] or name in terrain.types['topimage']):
        print "Warning: terrain sprites %s not used" %name
    terraingroups[name] = []
    images = getimages(terraindir, colorkey=MAGENTA)
    for image in images:
        numtiles = float(image.get_width())/image.get_height()
        if numtiles not in [1, 6]:
            print "Warning: sprite has invalid size"
            continue
        sprite = dirsprites(image) if numtiles == 6 else image
        terraingroups[name].append(sprite)

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
Unknown = pathimage('tiles', 'overlays', 'Unknown.png')
NonVisible = pathimage('tiles', 'overlays', 'NonVisible.png', alpha=True)

# These two can be randomly chosen
Damaged = getimages(os.path.join('tiles', 'overlays', 'damaged'), alpha=True)
Burning = getimages(os.path.join('tiles', 'overlays', 'fire'), alpha=True)

def rotatedquad(image, direction):
    """Return {direction: sprite} for rotations at right-angles to 'direction'"""
    rotcoord = lambda coord: (coord[1], -coord[0])
    rdict = {}
    for count in range(4):
        rdict[direction] = pygame.transform.rotate(image, 90*count)
        direction = rotcoord(direction)
    return rdict

# Overlays for fuses.
FuseLeft = pathimage('tiles', 'overlays', 'Fuse.png', alpha=True)
Fuse = rotatedquad(FuseLeft, LEFT)

# Overlays for tiles with collectables.
Coin = pathimage('tiles', 'collectables', 'Coin.png', alpha=True)
Choc = pathimage('tiles', 'collectables', 'Chocolate.png', alpha=True)
Dynamite = pathimage('tiles', 'collectables', 'Dynamite.png', alpha=True)

Collectables = {
    collectables.COIN: Coin,
    collectables.CHOCOLATE: Choc,
    collectables.DYNAMITE: Dynamite
}

def loadgemgo(name):
    return pathimage('tiles', 'gemgos', name+'.png', alpha=True)

# Player sprites.
PlayerLeft = loadgemgo('Player')
PlayerRight = pygame.transform.flip(PlayerLeft, True, False)

# Bear sprites.
BearLeft = loadgemgo('Bear')
BearRight = pygame.transform.flip(BearLeft, True, False)

# Dragon sprites.
DragonRed = rotatedquad(loadgemgo('Dragon-Red'), UPLEFT)

Sign = loadgemgo('Sign')

PixieLeft = loadgemgo('Pixie')
PixieRight = pygame.transform.flip(PixieLeft, True, False)

DuckieLeft = loadgemgo('Duckie')
DuckieRight = pygame.transform.flip(DuckieLeft, True, False)

Portal = chopimage(loadgemgo('Portal'), 3, 4)
