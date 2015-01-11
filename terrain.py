import numpy
import pygame.surfarray

import images

celltypefields = [
    ('destructable',    numpy.bool_),
    ('fireignitechance',numpy.float_),
    ('fireoutchance',   numpy.float_),
    ('covered',         numpy.bool_),
    ('transparent',     numpy.bool_),
    ('solid',           numpy.bool_),
    ('temperature',     numpy.int8 ),
    ('sogginess',       numpy.uint8),
    ('roughness',       numpy.uint8)
]

csvcolorfields = [
    ('r',               numpy.uint8),
    ('g',               numpy.uint8),
    ('b',               numpy.uint8)
]

csvimagefields = [
    ('groundimage',    (numpy.str_, 20)),
    ('topimage',       (numpy.str_, 20))
]

csvdtype = numpy.dtype(csvcolorfields + celltypefields + csvimagefields)

types = numpy.genfromtxt('map/terrain.csv', delimiter=',', dtype=csvdtype, autostrip=True)
typeslist = types.tolist()

def colorlist(surface):
    return pygame.surfarray.map_array(surface, types[['r','g','b']].view(numpy.uint8).reshape(-1, 3))
def color_typeindex(surface):
    return zip(colorlist(surface), range(len(typeslist)))

typeimages = []
for type in types:
    typeimages.append((
        images.terrain[type['groundimage']],
        images.terrain[type['topimage']]
        ))

cellstatefields = [
    ('explored',        numpy.bool_),
    ('collectableitem', numpy.int8)
]

cellimagefields = [
    ('layeroffset',     numpy.int_),
    ('groundimage',     numpy.object),
    ('topimage',        numpy.object)
]

celldtype = numpy.dtype(cellstatefields + celltypefields + cellimagefields)

def copyfill(i):
    colorlen = len(csvcolorfields)
    layeroffset = (len(types)/2-i[0],)
    return (0,)*len(cellstatefields) + i[1][colorlen:colorlen+len(celltypefields)] + layeroffset + typeimages[i[0]]
typeindextocell = numpy.array([copyfill(i) for i in enumerate(typeslist)], dtype=celldtype)
