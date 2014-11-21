import numpy

csvdtype = numpy.dtype([
    ('r',               numpy.uint8),
    ('g',               numpy.uint8),
    ('b',               numpy.uint8),
    ('name',           (numpy.str_, 19)),
    ('top',             numpy.bool_),
    ('destructable',    numpy.bool_),
    ('temperature',     numpy.int8),
    ('fireignitechance',numpy.float_),
    ('fireoutchance',   numpy.float_),
    ('hasroof',         numpy.bool_),
    ('difficulty',      numpy.int8),
    ('transparent',     numpy.bool_),
    ('solid',           numpy.bool_),
    ('sogginess',       numpy.bool_),
    ('groundimage',    (numpy.str_, 20)),
    ('topimage',       (numpy.str_, 20))
    ])

types = numpy.genfromtxt('map/terrain.csv', delimiter=',', dtype=csvdtype, autostrip=True)
typeslist = types.tolist()
def mapcolor(color):
    return (color[0] << 16) + (color[1] << 8) + color[2]
color_typeindex = [(mapcolor(i[1][0:3]), i[0]) for i in enumerate(typeslist)]

typetoimageindex = {
    'groundimage': [],
    'topimage'   : []
}

celldtype = numpy.dtype([
    ('damaged',         numpy.bool_),
    ('burning',         numpy.bool_),
    ('explored',        numpy.bool_),
    ('collectableitem', numpy.int8),
    ('name',           (numpy.str_, 19)),
    ('top',             numpy.bool_),
    ('destructable',    numpy.bool_),
    ('temperature',     numpy.int8),
    ('fireignitechance',numpy.float_),
    ('fireoutchance',   numpy.float_),
    ('hasroof',         numpy.bool_),
    ('difficulty',      numpy.int8),
    ('transparent',     numpy.bool_),
    ('solid',           numpy.bool_),
    ('sogginess',       numpy.bool_),
    ('groundimage',     numpy.uint8),
    ('topimage',        numpy.uint8),
    ('random',          numpy.uint8),
    ])

typeindextocell = numpy.array([(0,0,0,0)+i[1][3:14]+(i[0],0,0) for i in enumerate(typeslist)], dtype=celldtype)
