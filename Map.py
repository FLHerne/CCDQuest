import pygame
import random
import CellFiller
from colors import *
import collectables
import images
import numpy
import os.path
import sys

class Map():
    '''Contains array of Cells and properties representing the map as a whole'''
    CELLDAMAGEDCOST = 5
    CELLBURNINGCOST = 200

    def __init__(self, mapdict):
        '''Load the map from image files'''
        self.startpos = tuple(mapdict['startpos'])
        self.signdefs = []
        if 'signs' in mapdict:
            self.signdefs = mapdict['signs']
        self.origcoins = 0
        self.burningtiles = set()
        self.crcount = 0

        celldtype = numpy.dtype([
            ('damaged',         numpy.bool_),
            ('burning',         numpy.bool_),
            ('explored',        numpy.bool_),
            ('visible',         numpy.bool_),
            ('collectableitem', numpy.int8),
            ('name',           (numpy.str_, 19)),
            ('top',             numpy.bool_),
            ('destructable',    numpy.bool_),
            ('temperature',     numpy.int8),
            ('fireignitechance',numpy.float),
            ('fireoutchance',   numpy.float),
            ('hasroof',         numpy.bool_),
            ('difficulty',      numpy.int8),
            ('transparent',     numpy.bool_),
            ('solid',           numpy.bool_),
            ('groundimage',     numpy.uint8),
            ('topimage',        numpy.uint8),
            ('random',          numpy.int8)
            ])

        terrainfilepath = os.path.join('map', mapdict['dir'], mapdict['terrainfile'])
        itemfilepath = os.path.join('map', mapdict['dir'], mapdict['itemfile'])
        for filepath in terrainfilepath, itemfilepath:
            if not os.path.isfile(filepath):
                print "Failed to load map:"
                print filepath, "is not a file"
                sys.exit(1)

        binaryfilepath = None
        if 'binaryfile' in mapdict:
            binaryfilepath = os.path.join('map', mapdict['dir'], mapdict['binaryfile'])
        if  (binaryfilepath and os.path.isfile(binaryfilepath) and
             os.path.getmtime(binaryfilepath) >= os.path.getmtime(terrainfilepath) and
             os.path.getmtime(binaryfilepath) >= os.path.getmtime(itemfilepath)):
            self.cellarray = numpy.load(binaryfilepath)
            self.size = self.cellarray.shape

        else:
            groundimage = pygame.image.load(terrainfilepath).convert()
            groundarray = pygame.surfarray.pixels2d(groundimage)
            collectablesimage = pygame.image.load(itemfilepath).convert()
            collectablesarray = pygame.surfarray.pixels2d(collectablesimage)
            self.size = list(groundimage.get_rect().size)
            def createcell(ground, collectable):
                return list((0,0,0,0) + CellFiller.collectablet[collectable] + CellFiller.terraint[ground] + (random.randint(0, 255),))
            procfunc = numpy.frompyfunc(createcell, 2, 1)
            temparr = procfunc(groundarray, collectablesarray)
            self.cellarray = numpy.ndarray(self.size, dtype=celldtype)
            for x in xrange(0, self.size[0]):
                for y in xrange(0, self.size[1]):
                    tempval = tuple(temparr[x][y])
                    self.cellarray[x][y] = tempval
            if binaryfilepath:
                print "Creating binary map file:", binaryfilepath
                numpy.save(binaryfilepath, self.cellarray)

        self.origcoins = (self.cellarray['collectableitem'] == collectables.COIN).sum()

    def __getitem__(self, coord):
        '''Get map item with [], wrapping'''
        return self.cellarray[coord[0]%self.size[0]][coord[1]%self.size[1]]

    def __setitem__(self, coord, value):
        '''Set map item with [], wrapping'''
        self.cellarray[coord[0]%self.size[0]][coord[1]%self.size[1]] = value

    def sprites(self, coord):
        sprites = []
        def addsprite(sprite, layer):
            sprites.append((sprite,
                            (coord[0]*images.TILESIZE + (images.TILESIZE-sprite.get_width())/2,
                             coord[1]*images.TILESIZE + (images.TILESIZE-sprite.get_height())/2),
                            layer))
        cell = self[coord]
        if not cell['explored']:
            addsprite(images.Unknown, -10)
            return sprites
        for image in cell['groundimage'], cell['topimage']:
            if image == 255:
                continue
            spritelist = images.Terrain[image]
            spritelistindex = (cell['random']%len(spritelist))
            sprite = spritelist[spritelistindex]
            addsprite(sprite, -10)
        if cell['damaged']:
            addsprite(images.Damaged, -9)
        if cell['collectableitem'] != 0:
            addsprite(images.Collectables[cell['collectableitem']], -8)
        if cell['burning']:
            addsprite(images.Burning, -9)
        if not cell['visible']:
            addsprite(images.NonVisible, 50)
        return sprites

    def destroy(self, coord):
        '''Change cell attributes to reflect destruction'''
        cell = self[coord]
        if not cell['destructable']:
            return False
        cell['damaged'] = True
        cell['hasroof'] = False
        cell['name'] = "shattered debris"
        cell['collectableitem'] = 0
        cell['top'] = False
        cell['fireignitechance'] = 0
        cell['fireoutchance'] = 1
        cell['transparent'] = True
        cell['solid'] = False
        cell['difficulty'] += Map.CELLDAMAGEDCOST
        return True

    def ignite(self, coord, multiplier=1, forceignite=False):
        '''Start a fire at coord, with chance cell.firestartchance * multiplier'''
        cell = self[coord]
        if cell['collectableitem'] == collectables.DYNAMITE:
            self.detonate(coord)
        if forceignite or random.random() < cell['fireignitechance'] * multiplier:
            cell['burning'] = True
            if cell['fireignitechance'] > 0:
                self.destroy(coord)
            self.burningtiles.add((coord[0]%self.size[0], coord[1]%self.size[1]))
            return True
        return False

    def detonate(self, coord):
        '''Set off an explosion at coord'''
        def blam(epicentre):
            self[epicentre]['collectableitem'] = 0
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    curpos = (epicentre[0]+dx, epicentre[1]+dy)
                    if not self.ignite(curpos, multiplier=3):
                        self.destroy(curpos)
        if not self[coord]['destructable']:
            return False
        blam(coord)
        return True

    def update(self):
        '''Spread fire, potentially other continuous map processes'''
        for tile in self.burningtiles.copy():
            cell = self[tile]
            for nbrpos in [(tile[0]-1, tile[1]), (tile[0], tile[1]-1), (tile[0]+1, tile[1]), (tile[0], tile[1]+1)]:
                self.ignite(nbrpos)
            if random.random() < cell['fireoutchance']:
                cell['burning'] = False
                self.burningtiles.remove(tile)
