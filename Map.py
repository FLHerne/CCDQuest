import pygame
import random
from colors import *
import directions
import coords
import collectables
import images
import numpy
import os.path
import sys
from images import TerrainIndex as Index

class Map():
    """Contains array of Cells and properties representing the map as a whole"""
    CELLDAMAGEDCOST = 5
    CELLBURNINGCOST = 200
    DIRTYCACHE = False

    def __init__(self, mapdict):
        """Load the map from image files"""
        self.startpos = tuple(mapdict['startpos'])
        self.signdefs = []
        if 'signs' in mapdict:
            self.signdefs = mapdict['signs']
        self.pixiedefs = []
        if 'pixies' in mapdict:
            self.pixiedefs = mapdict['pixies']
        self.origcoins = 0
        self.burningtiles = set()
        self.fusetiles = set()
        self.crcount = 0

        celldtype = numpy.dtype([
            ('damaged',         numpy.bool_),
            ('burning',         numpy.bool_),
            ('explored',        numpy.bool_),
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

        terraint = numpy.array([
            (0,0,0,0, 'wall', False, True, 20, 0, 1, False, 3, False, True, Index['wall'], 255, 0),
            (0,0,0,0, 'rocky ground', False, True, 20, 0, 1, False, 5, True, False, Index['rock'], 255, 0),
            (0,0,0,0, 'wooden planking', False, True, 20, 0.4, 0.1, False, 2, True, False, Index['planks'], 255, 0),
            (0,0,0,0, 'snow', False, True, -5, 0, 1, False, 4, True, False, Index['snow'], 255, 0),
            (0,0,0,0, 'water', False, False, 12, 0, 1, False, 25, True, False, Index['water'], 255, 0),
            (0,0,0,0, 'deep water', False, False, 8, 0, 1, False, 25, True, True, Index['deepwater'], 255, 0),
            (0,0,0,0, 'grass', False, True, 20, 0.1, 0.3, False, 2, True, False, Index['grass'], 255, 0),
            (0,0,0,0, 'marshland', False, True, 20, 0, 1, False, 20, True, False, Index['marsh'], 255, 0),
            (0,0,0,0, 'window', False, True, 20, 0, 1, False, 3, True, True, Index['glass'], 255, 0),
            (0,0,0,0, 'forest', True, True, 20, 0.5, 0.1, False, 8, False, False, Index['grass'], Index['tree'], 0),
            (0,0,0,0, 'sand', False, True, 20, 0, 1, False, 3, True, False, Index['sand'], 255, 0),
            (0,0,0,0, 'paving', False, True, 20, 0, 1, False, 1, True, False, Index['paving'], 255, 0),
            (0,0,0,0, 'floor', False, True, 20, 0.5, 0.05, True, 1, True, False, Index['floor'], 255, 0)
            ], celldtype)

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
             os.path.getmtime(binaryfilepath) >= os.path.getmtime(itemfilepath) and
             not Map.DIRTYCACHE):
            self.cellarray = numpy.load(binaryfilepath)
            self.size = self.cellarray.shape

        else:
            groundimage = pygame.image.load(terrainfilepath).convert()
            groundarray = pygame.surfarray.pixels2d(groundimage)
            collectablesimage = pygame.image.load(itemfilepath).convert()
            collectablesarray = pygame.surfarray.pixels2d(collectablesimage)
            self.size = list(groundimage.get_rect().size)

            def mapcolor(color):
                return (color[0] << 16) + (color[1] << 8) + color[2]
            indexarray = numpy.empty(self.size, numpy.int8)
            colorindex = [
                BLACK, GREY, BROWN, WHITE, LIGHTBLUE, BLUE, GREEN,
                BLUEGREY, CYAN, DARKGREEN, DARKYELLOW, LIGHTYELLOW, DARKPINK
                ]
            for i in range(0, len(colorindex)):
                color = mapcolor(colorindex[i])
                indexarray[groundarray == color] = i

            self.cellarray = numpy.choose(indexarray, terraint)

            colorindex = [
                WHITE, YELLOW, BROWN, RED
                ]
            for i in range(0, len(colorindex)):
                color = mapcolor(colorindex[i])
                self.cellarray['collectableitem'][collectablesarray == color] = i

            if binaryfilepath:
                print "Creating binary map file:", binaryfilepath
                numpy.save(binaryfilepath, self.cellarray)

        self.origcoins = (self.cellarray['collectableitem'] == collectables.COIN).sum()

    def __getitem__(self, coord):
        """Get map item with [], wrapping"""
        return self.cellarray[coord[0]%self.size[0]][coord[1]%self.size[1]]

    def __setitem__(self, coord, value):
        """Set map item with [], wrapping"""
        self.cellarray[coord[0]%self.size[0]][coord[1]%self.size[1]] = value

    def sprites(self, coord):
        sprites = []
        def addsprite(image, layer):
            sprites.append((image,
                            (coord[0]*images.TILESIZE + (images.TILESIZE-image.get_width())/2,
                             coord[1]*images.TILESIZE + (images.TILESIZE-image.get_height())/2),
                            layer))
        cell = self[coord]
        if not cell['explored']:
            addsprite(images.Unknown, -20)
            return sprites
        def pickrandomsprite(spritelist):
            return spritelist[cell['random']%len(spritelist)]
        for imagelayer in (cell['groundimage'], -10), (cell['topimage'], 10):
            if imagelayer[0] == 255:
                continue
            offsetspritelist = images.TerrainSprites[imagelayer[0]]
            addsprite(pickrandomsprite(offsetspritelist[1]), imagelayer[1]+offsetspritelist[0])
        if cell['damaged']:
            addsprite(pickrandomsprite(images.Damaged), -3)
        if coord in self.fusetiles:
            for direction in directions.CARDINALS:
                nbrcoord = coords.modsum(coord, direction, self.size)
                if nbrcoord in self.fusetiles or self[nbrcoord]['collectableitem'] == collectables.DYNAMITE:
                    addsprite(images.Fuse[direction], -2)
        if cell['collectableitem'] != 0:
            addsprite(images.Collectables[cell['collectableitem']], -1)
        if cell['burning']:
            addsprite(pickrandomsprite(images.Burning), -1)
        return sprites

    def placefuse(self, coord):
        self.fusetiles.add(coords.mod(coord, self.size))

    def ignitefuse(self, coord):
        coord = coords.mod(coord, self.size)
        if self[coord]['collectableitem'] == collectables.DYNAMITE:
            self.detonate(coord)
        if not coord in self.fusetiles:
            return False
        openlist = set()
        openlist.add(coord)
        while len(openlist) > 0:
            curpos = openlist.pop()
            if curpos in self.fusetiles:
                self.fusetiles.remove(curpos)
            for nbrpos in coords.neighbours(curpos):
                if self[nbrpos]['collectableitem'] == collectables.DYNAMITE:
                    self.detonate(nbrpos)
                nbrpos = coords.mod(nbrpos, self.size)
                if nbrpos in self.fusetiles:
                    openlist.add(nbrpos)

    def destroy(self, coord):
        """Change cell attributes to reflect destruction"""
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
        cell['topimage'] = 255
        return True

    def ignite(self, coord, multiplier=1, forceignite=False):
        """Start a fire at coord, with chance cell.firestartchance * multiplier"""
        coord = coords.mod(coord, self.size)
        cell = self[coord]
        if coord in self.fusetiles:
            self.ignitefuse(coord)
        if cell['collectableitem'] == collectables.DYNAMITE:
            self.detonate(coord)
        if forceignite or random.random() < cell['fireignitechance'] * multiplier:
            cell['burning'] = True
            if cell['fireignitechance'] > 0:
                self.destroy(coord)
            self.burningtiles.add(coord)
            return True
        return False

    def detonate(self, coord):
        """Set off an explosion at coord"""
        def blam(epicentre):
            self[epicentre]['collectableitem'] = 0
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    curpos = coords.sum(epicentre, (dx, dy))
                    if not self.ignite(curpos, multiplier=3):
                        self.destroy(curpos)
        if not self[coord]['destructable']:
            return False
        blam(coord)
        return True

    def update(self):
        """Spread fire, potentially other continuous map processes"""
        for tile in self.burningtiles.copy():
            cell = self[tile]
            for nbrpos in coords.neighbours(tile):
                self.ignite(nbrpos)
            if random.random() < cell['fireoutchance']:
                cell['burning'] = False
                self.burningtiles.remove(tile)
