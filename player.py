import pygame

def player:
    def __init__(self, position, colour, visibility):
        self.position = position
        self.colour = colour
        self.visibility = visibility
    def draw(drawsurface):
        '''draw the player as a blinking circle'''
        if RealMap[Pos[0], Pos[1]].top == False:
            x = ((self.position[0]*BLOCKSIZE)+int(BLOCKSIZE/2))
            y = ((self.position[1]*BLOCKSIZE)+int(BLOCKSIZE/2))
            radius = int(BLOCKSIZE/2)
            pygame.draw.circle(drawSurface, MAGEN, (x%world.get_width(), y%world.get_height()), radius)
            