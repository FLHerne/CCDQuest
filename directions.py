import coords

NONE      = ( 0, 0)

UP        = ( 0,-1)
DOWN      = ( 0, 1)
LEFT      = (-1, 0)
RIGHT     = ( 1, 0)

UPLEFT    = (-1,-1)
UPRIGHT   = ( 1,-1)
DOWNLEFT  = (-1, 1)
DOWNRIGHT = ( 1, 1)

cardinals = [UP, DOWN, LEFT, RIGHT]
ordinals = [UPLEFT, UPRIGHT, DOWNLEFT, DOWNRIGHT]
principles = cardinals + ordinals

def perpendiculars(direction):
    swapaxes = direction[::-1]
    return tuple([swapaxes, coords.multuple(swapaxes, -1)])
