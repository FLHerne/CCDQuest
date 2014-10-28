import pygame
import random
import CellFiller
from colors import *
import collectables
import images
import numpy
import os.path

class Map():
    '''Contains array of Cells and properties representing the map as a whole'''
    CELLDAMAGEDCOST = 5
    CELLBURNINGCOST = 200

    def __init__(self, mapdict):
        '''Load the map from image files'''
        self.startpos = tuple(mapdict['startpos'])
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
            ('image',           numpy.int8),
            ('random',          numpy.int8)
            ])

        if 'binaryfile' in mapdict and os.path.isfile(mapdict['binaryfile']):
            self.cellarray = numpy.load(mapdict['binaryfile'])
            self.size = self.cellarray.shape

        else:
            groundimage = pygame.image.load(mapdict['terrainfile']).convert()
            groundarray = pygame.surfarray.pixels2d(groundimage)
            collectablesimage = pygame.image.load(mapdict['itemfile']).convert()
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
            if 'binaryfile' in mapdict:
                print "Creating binary map file:", mapdict['binaryfile']
                numpy.save(mapdict['binaryfile'], self.cellarray)

        self.origcoins = (self.cellarray['collectableitem'] == collectables.COIN).sum()

    def __getitem__(self, coord):
        '''Get map item with [], wrapping'''
        return self.cellarray[coord[0]%self.size[0]][coord[1]%self.size[1]]

    def __setitem__(self, coord, value):
        '''Set map item with [], wrapping'''
        self.cellarray[coord[0]%self.size[0]][coord[1]%self.size[1]] = value

    def draw(self, drawSurface, coord):
        '''Blit cell graphics to the specified surface'''
        Drawx = coord[0]*images.TILESIZE
        Drawy = coord[1]*images.TILESIZE
        DrawPos = (Drawx, Drawy)
        cell = self[coord]
        if not cell['explored']:
            drawSurface.blit(images.Unknown, DrawPos)
            return
        spritelist = images.Terrain[cell['image']]
        spritelistindex = (cell['random']%len(spritelist))
        sprite = spritelist[spritelistindex]
        Drawxoffset = (images.TILESIZE-sprite.get_width())/2
        Drawyoffset = (images.TILESIZE-sprite.get_height())/2
        drawSurface.blit(sprite, (Drawx+Drawxoffset, Drawy+Drawyoffset))
        if cell['damaged']:
            drawSurface.blit(images.Damaged, DrawPos)
        if cell['collectableitem'] != 0:
            drawSurface.blit(images.Collectables[cell['collectableitem']], DrawPos)
        if cell['burning']:
            drawSurface.blit(images.Burning, DrawPos)
        if not cell['visible']:
            drawSurface.blit(images.NonVisible, DrawPos)

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
