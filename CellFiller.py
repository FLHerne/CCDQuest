from colors import *
import collectables
from images import TerrainIndex as Index

def mapcolor(color):
    return (color[0] << 16) + (color[1] << 8) + color[2]

terraint = {
    # name top destructable temperature fireignitechance fireoutchance hasroof difficulty transparent solid
    mapcolor(BLACK):
        ('wall', False, True, 20, 0, 1, False, 3, False, True, Index['wall'], 255),
    mapcolor(GREY):
        ('rocky ground', False, True, 20, 0, 1, False, 5, True, False, Index['rock'], 255),
    mapcolor(BROWN):
        ('wooden planking', False, True, 20, 0.4, 0.1, False, 2, True, False, Index['planks'], 255),
    mapcolor(WHITE):
        ('snow', False, True, -5, 0, 1, False, 4, True, False, Index['snow'], 255),
    mapcolor(LIGHTBLUE):
        ('water', False, False, 12, 0, 1, False, 25, True, False, Index['water'], 255),
    mapcolor(BLUE):
        ('deep water', False, False, 8, 0, 1, False, 25, True, True, Index['deepwater'], 255),
    mapcolor(GREEN):
        ('grass', False, True, 20, 0.1, 0.3, False, 2, True, False, Index['grass'], 255),
    mapcolor(BLUEGREY):
        ('marshland', False, True, 20, 0, 1, False, 20, True, False, Index['marsh'], 255),
    mapcolor(CYAN):
        ('window', False, True, 20, 0, 1, False, 3, True, True, Index['glass'], 255),
    mapcolor(DARKGREEN):
        ('forest', True, True, 20, 0.5, 0.1, False, 8, False, False, Index['grass'], Index['tree']),
    mapcolor(DARKYELLOW):
        ('sand', False, True, 20, 0, 1, False, 3, True, False, Index['sand'], 255),
    mapcolor(LIGHTYELLOW):
        ('paving', False, True, 20, 0, 1, False, 1, True, False, Index['paving'], 255),
    mapcolor(DARKPINK):
        ('floor', False, True, 20, 0.5, 0.05, True, 1, True, False, Index['floor'], 255)
}

collectablet = {
    mapcolor(WHITE): (0,),
    mapcolor(MAGENTA): (0,),
    mapcolor(YELLOW): (collectables.COIN,),
    mapcolor(BROWN): (collectables.CHOCOLATE,),
    mapcolor(RED): (collectables.DYNAMITE,)
}
