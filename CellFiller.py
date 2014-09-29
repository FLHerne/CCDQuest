from colors import *
import collectables

class CellFiller:
    def __init__(self, groundcolor, collectablecolor):
        '''Set up initial attributes'''
        self.damaged = False
        self.burning = False
        self.explored = False
        self.visible = False
        self.name = "UNNAMED TERRAIN"
        self.collectableitem = 0
        self.top = False
        self.destructable = True
        self.temperature = 20
        self.fireignitechance = 0
        self.fireoutchance = 1
        self.hasroof = False
        if groundcolor == BLACK:
            self.transparent = False
            self.solid = True
            self.difficulty = 3
        elif groundcolor == GREY:
            self.transparent = True
            self.solid = False
            self.difficulty = 5
            self.name = "rocky ground"
        elif groundcolor == BROWN:
            self.transparent = True
            self.solid = False
            self.difficulty = 2
            self.name = "wooden planking"
            self.fireignitechance = 0.4
            self.fireoutchance = 0.1
        elif groundcolor == WHITE:
            self.transparent = True
            self.solid = False
            self.difficulty = 4
            self.name = "snow"
            self.temperature = -5
        elif groundcolor == LIGHTBLUE:
            self.transparent = True
            self.solid = False
            self.difficulty = 25
            self.name = "water"
            self.destructable = False
            self.temperature = 12
        elif groundcolor == BLUE:
            self.transparent = True
            self.solid = True
            self.difficulty = 25
            self.name = "deep water"
            self.destructable = False
            self.temperature = 8
        elif groundcolor == GREEN:
            self.transparent = True
            self.solid = False
            self.difficulty = 2
            self.name = "grass"
            self.fireignitechance = 0.1
            self.fireoutchance = 0.3
        elif groundcolor == BLUEGREY:
            self.transparent = True
            self.solid = False
            self.difficulty = 20
            self.name = "marshland"
        elif groundcolor == CYAN:
            self.transparent = True
            self.solid = True
            self.difficulty = 3
            self.name = "window"
        elif groundcolor == DARKGREEN:
            self.transparent = False
            self.solid = False
            self.difficulty = 8
            self.name = "forest"
            self.fireignitechance = 0.5
            self.fireoutchance = 0.1
            self.top = True
        elif groundcolor == DARKYELLOW:
            self.transparent = True
            self.solid = False
            self.difficulty = 3
            self.name = "sand"
        elif groundcolor == LIGHTYELLOW:
            self.transparent = True
            self.solid = False
            self.difficulty = 1
            self.name = "paving"
        elif groundcolor == DARKPINK:
            self.transparent = True
            self.solid = False
            self.difficulty = 1
            self.name = "floor"
            self.fireignitechance = 0.5
            self.fireoutchance = 0.05
            self.hasroof = True
        else:
            raise Exception("Unknown map color")

        if collectablecolor == YELLOW:
            self.collectableitem = collectables.COIN
        elif collectablecolor == BROWN:
            self.collectableitem = collectables.CHOCOLATE
        elif collectablecolor == RED:
            self.collectableitem = collectables.DYNAMITE

    def totuple(self):
        return (
            self.damaged, #0
            self.burning, #0
            self.explored, #0
            self.visible, #0
            self.name, #typefixed
            self.collectableitem, #instance
            self.top, #typefixed
            self.destructable, #typefixed
            self.temperature, #typefixed
            self.fireignitechance, #typefixed
            self.fireoutchance, #typefixed
            self.hasroof, #typefixed
            self.difficulty, #typefixed
            self.transparent, #typefixed
            self.solid #typefixed
            )
