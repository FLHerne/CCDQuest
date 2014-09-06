import pygame

def player:
    def __init__(self, position, colour, visibility):
        self.position = position
        self.colour = colour
        self.visibility = visibility
        self.visibletiles = []
    def draw(drawsurface):
        '''draw the player as a blinking circle'''
        if RealMap[Pos[0], Pos[1]].top == False:
            x = ((self.position[0]*BLOCKSIZE)+int(BLOCKSIZE/2))
            y = ((self.position[1]*BLOCKSIZE)+int(BLOCKSIZE/2))
            radius = int(BLOCKSIZE/2)
            pygame.draw.circle(drawSurface, MAGEN, (x%world.get_width(), y%world.get_height()), radius)
    def UpdateVisible():
        '''update the visibility of cells by the player'''
        for x in range(Pos[0]-VISIBILITY-1, Pos[0]+VISIBILITY+2):
            for y in range(Pos[1]-VISIBILITY-1, Pos[1]+VISIBILITY+2):
                RealMap[x, y].visible = False
        CrossCheck()
        DiagonalCheck()
        for tile in visible_tiles(player1.pos, 15, map):
            map[tile].visible = True map[tile].explored = True'