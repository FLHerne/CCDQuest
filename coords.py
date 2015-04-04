import __builtin__
import directions

def sum(*args):
    """Element-wise sum of (equal-size) tuples"""
    return tuple(map(__builtin__.sum, zip(*args)))

def mod(a, b):
    """Element-wise modulo of a with b"""
    return tuple([ea%eb for ea, eb in zip(a, b)])

def modsum(*args):
    """Sum all but the last argument, modulo by that"""
    modval = args[-1]
    args = args[:-1]
    return mod(sum(*args), modval)

def mul(a, b):
    """Element-wise multiple of a by b (tuple or int)"""
    try:
        return tuple([ea*b for ea in a])
    except TypeError:
        return tuple([ea*eb for ea, eb in zip(a, b)])

def neighbours(a):
    """List of 4 tiles neighbouring a"""
    return [sum(a, dir) for dir in directions.CARDINALS]

def mindist(a, b, size):
    """Distance per axis between two points accounting for world wrapping"""
    return tuple([min((eb-ea)%es, (ea-eb)%es) for ea, eb, es in zip(a, b, size)])

def tileoffset(a, b, size):
    """Offset of b from a, accounting for wrapping of world size"""
    offset = [0, 0]
    for axis in [0, 1]:
        subtract = b[axis] - a[axis]
        absubtract = abs(subtract)
        if absubtract*2 <= size[axis]:
            offset[axis] = subtract
        else:
            offset[axis] = (size[axis]-absubtract) * cmp(0, subtract)
    return offset
