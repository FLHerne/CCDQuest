import numpy
import pygame.surfarray
from colors import *

NONE = 0
COIN = 1
CHOCOLATE = 2
DYNAMITE = 3

mapcolor = {
    WHITE:  NONE,
    YELLOW: COIN,
    BROWN:  CHOCOLATE,
    RED:    DYNAMITE
}
def colorlist(surface):
    return [pygame.surfarray.map_array(surface, numpy.array([color])) for color in mapcolor.keys()]

value = {
    NONE: 0,
    COIN: 1,
    CHOCOLATE: 50,
    DYNAMITE: 1
}

name = {
    NONE: "",
    COIN: "a coin",
    CHOCOLATE: "some chocolate",
    DYNAMITE: "a stick of dynamite"
    }