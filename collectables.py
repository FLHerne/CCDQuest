from colors import *
import terrain

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
colorlist = [terrain.mapcolor(color) for color in mapcolor.keys()]

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