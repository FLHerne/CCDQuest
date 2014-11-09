import numpy

csvdtype = numpy.dtype([
    ('r',               numpy.uint8),
    ('g',               numpy.uint8),
    ('b',               numpy.uint8),
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
    ('groundimage',    (numpy.str_, 20)),
    ('topimage',       (numpy.str_, 20))
    ])

types = numpy.genfromtxt('map/terrain.csv', delimiter=',', dtype=csvdtype, autostrip=True)
