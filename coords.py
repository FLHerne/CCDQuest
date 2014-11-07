import __builtin__
import directions

def sum(*args):
    '''Element-wise sum of (equal-size) tuples'''
    return tuple(map(__builtin__.sum, zip(*args)))

def mod(a, b):
    '''Element-wise modulo of a with b'''
    return tuple([ea%eb for ea, eb in zip(a, b)])

def mul(a, b):
    '''Element-wise multiple of a by b (tuple or int)'''
    try:
        return tuple([ea*b for ea in a])
    except TypeError:
        return tuple([ea*eb for ea, eb in zip(a, b)])

def neighbours(a):
    return [sum(a, dir) for dir in directions.CARDINALS]
